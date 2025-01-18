from rest_framework import mixins, viewsets

from open_democracy_back.models.questionnaire_and_profiling_models import (
    ProfilingQuestion,
    Role,
    ProfileType,
)
from open_democracy_back.serializers.questionnaire_and_profiling_serializers import (
    ProfilingQuestionSerializer,
    RoleSerializer,
    ProfileTypeSerializer,
)


class ProfilingQuestionView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ProfilingQuestionSerializer
    queryset = ProfilingQuestion.objects.all().prefetch_related(
        "categories",
        "response_choices",
        "roles",
        "surveys",
    )


class RoleView(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()


class ProfileTypeView(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ProfileTypeSerializer
    queryset = (
        ProfileType.objects.prefetch_related(
            "rules__conditional_question", "rules__response_choices"
        )
        .filter(questions_that_depend_on_me__isnull=False)
        .filter(rules__isnull=False)
        .all()
        .distinct()
    )
