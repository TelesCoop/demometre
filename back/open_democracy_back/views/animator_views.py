import re
from django.db.models import QuerySet, Q
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response as RestResponse
from rest_framework.exceptions import APIException
from my_auth.models import User
from open_democracy_back.exceptions import ErrorCode
from open_democracy_back.mixins.update_or_create_mixin import UpdateOrCreateModelMixin
from open_democracy_back.models import Assessment

from open_democracy_back.models.animator_models import Participant, Workshop
from open_democracy_back.models.participation_models import (
    Participation,
    ParticipationResponse,
)
from open_democracy_back.permissions import IsWorkshopExpert
from open_democracy_back.serializers.animator_serializers import (
    FullWorkshopSerializer,
    WorkshopParticipationResponseSerializer,
    WorkshopParticipationWithProfilingResponsesSerializer,
    WorkshopSerializer,
)
from open_democracy_back.utils import EMAIL_REGEX


class WorkshopView(
    mixins.ListModelMixin,
    UpdateOrCreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = WorkshopSerializer

    def get_queryset(self) -> QuerySet:
        return Workshop.objects.filter(
            Q(animator_id=self.request.user.id),
            Q(
                assessment__in=Assessment.objects.filter_has_details(
                    self.request.user.id
                )
            ),
        )

    def get_or_update_object(self, request):
        return self.get_queryset().get(
            id=request.data.get("id"),
        )

    @action(
        detail=False,
        methods=["GET"],
        url_path="by-assessment/(?P<assessment_id>.*)",
    )
    def for_assessment(self, request, assessment_id):
        assessments = Assessment.objects.filter_has_details(request.user.id).filter(
            pk=assessment_id
        )
        workshops = Workshop.objects.filter(assessment__in=assessments)
        return RestResponse(
            status=200,
            data=self.serializer_class(
                workshops, many=True, context=self.get_serializer_context()
            ).data,
        )


class FullWorkshopView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsWorkshopExpert]
    serializer_class = FullWorkshopSerializer

    def get_queryset(self) -> QuerySet:
        return Workshop.objects.filter(animator_id=self.request.user.id)


class WorkshopParticipationView(
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = WorkshopParticipationWithProfilingResponsesSerializer

    def get_queryset(self) -> QuerySet:
        qs = Participation.objects.filter(
            Q(workshop__animator_id=self.request.user.id)
            | Q(
                workshop__assessment__in=Assessment.objects.filter_has_details(
                    self.request.user.id
                )
            )
        )
        if self.action == "create":
            return qs.filter(workshop_id=self.request.data["workshop_id"])
        return qs

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            # Create or update a workshop participation with all its profiling responses

            # 1 - Retrieve Participant if exists or create new one
            email = request.data["participant_email"] or None
            name = request.data["participant_name"]
            try:
                participation_id = request.data.get("id")
                participation = self.get_queryset().get(id=participation_id)
                participant = participation.participant
                participant.name = name
                participant.email = email
                if medium := request.data.get("medium"):
                    participation.medium = medium
                participant.save()
            except ObjectDoesNotExist:
                # raise when we already have this participant email in this workshop
                if (
                    email
                    and self.get_queryset().filter(participant__email=email).exists()
                ):
                    raise APIException(
                        "Participant already exists for this workshop",
                        code=ErrorCode.PARTICIPANT_ALREADY_EXISTS,
                    )
                participant, new = Participant.objects.filter(
                    email__isnull=False
                ).update_or_create(email=email, defaults={"name": name})
                participation = Participation.objects.get_or_create(
                    participant_id=participant.id,
                    workshop_id=request.data["workshop_id"],
                    assessment_id=request.data["assessment_id"],
                    medium=request.data.get("medium"),
                )[0]

            # 2 - Update role of participant
            participation.role_id = request.data["role_id"]
            participation.save()

            # 3 - Pop responses from data before create or update participation (Otherwise serializer will reject it)
            responses_data = []
            if "responses" in request.data.keys():
                responses_data = request.data.pop("responses")

            # 4 - Create or update all profiling responses of participation
            for item in responses_data:
                if "participation_id" not in item:
                    item["participation_id"] = participation.id
                try:
                    participationResponse = participation.responses.get(
                        question_id=item["question_id"]
                    )
                    serializer = WorkshopParticipationResponseSerializer(
                        participationResponse, data=item
                    )
                except ObjectDoesNotExist:
                    serializer = WorkshopParticipationResponseSerializer(data=item)
                serializer.is_valid(raise_exception=True)
                serializer.save()

            return RestResponse(
                WorkshopParticipationWithProfilingResponsesSerializer(
                    participation
                ).data
            )


class WorkshopParticipationResponseView(
    mixins.ListModelMixin,
    UpdateOrCreateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsWorkshopExpert]
    serializer_class = WorkshopParticipationResponseSerializer

    def get_queryset(self, workshop_pk, participation_pk) -> QuerySet:
        return ParticipationResponse.objects.filter(
            participation__workshop__animator_id=self.request.user.id,
            participation__workshop_id=workshop_pk,
            participation_id=participation_pk,
        )

    def get_or_update_object(self, request, workshop_pk, participation_pk):
        return self.get_queryset(workshop_pk, participation_pk).get(
            participation_id=request.data.get("participation_id"),
            question_id=request.data.get("question_id"),
        )


class CloseWorkshopView(APIView):
    permission_classes = [IsWorkshopExpert]

    def patch(self, request, workshop_pk):
        with transaction.atomic():
            workshop = Workshop.objects.get(
                animator_id=self.request.user.id, id=workshop_pk
            )
            workshop.closed = True
            workshop.save()

            for participation in workshop.participations.all():
                # if there is a email create user or retrieve existing user and attribut him the participation
                if participation.participant.email:
                    if not re.fullmatch(EMAIL_REGEX, participation.participant.email):
                        raise APIException(
                            detail=f"The email is not valid shape : {participation.participant.email}",
                            code=ErrorCode.INVALID_EMAIL_SHAPE.value,
                        )
                    user, _ = User.objects.get_or_create(
                        email=participation.participant.email,
                        defaults={"username": participation.participant.email},
                    )
                    participation.user = user
                    participation.save()
                    # TODO : what append if there is a participation with this user and this assessment (like this it breaks)

            serializer = WorkshopSerializer(workshop)
            return RestResponse(serializer.data, status=status.HTTP_200_OK)
