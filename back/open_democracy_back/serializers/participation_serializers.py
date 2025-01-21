from django.utils import timezone
from rest_framework import serializers
from open_democracy_back.exceptions import ErrorCode

from open_democracy_back.models import Assessment
from open_democracy_back.models.assessment_models import AssessmentResponse

from open_democracy_back.models.participation_models import (
    ClosedWithScaleCategoryResponse,
    Participation,
    ParticipationResponse,
    ParticipationPillarCompleted,
)
from open_democracy_back.models.questionnaire_and_profiling_models import (
    Category,
    Role,
    Question,
    ResponseChoice,
)

RESPONSE_FIELDS = [
    "id",
    "question_id",
    "has_passed",
    "unique_choice_response_id",
    "multiple_choice_response_ids",
    "boolean_response",
    "percentage_response",
    "number_response",
    "closed_with_scale_response_categories",
]
OPTIONAL_RESPONSE_FIELDS = [
    "unique_choice_response_id",
    "multiple_choice_response_ids",
    "boolean_response",
    "percentage_response",
    "closed_with_scale_response_categories",
]


class AssessmentField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return Assessment.objects.filter(initialization_date__lte=timezone.now())


class ParticipationField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return Participation.objects.filter(
            user_id=self.context.get("request").user.id,
            assessment__initialization_date__lte=timezone.now(),
        )


class ParticipationPillarCompletedSerializer(serializers.ModelSerializer):
    participation_id = serializers.PrimaryKeyRelatedField(
        source="participation", read_only=True
    )
    pillar_id = serializers.PrimaryKeyRelatedField(source="pillar", read_only=True)

    class Meta:
        model = ParticipationPillarCompleted
        fields = ["participation_id", "pillar_id", "completed"]


class ParticipationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    assessment_id = AssessmentField(source="assessment")
    role_id = serializers.PrimaryKeyRelatedField(
        source="role", queryset=Role.objects.all()
    )
    is_pillar_questions_completed = ParticipationPillarCompletedSerializer(
        source="participationpillarcompleted_set", many=True, read_only=True
    )
    profile_ids = serializers.PrimaryKeyRelatedField(
        read_only=True, source="profiles", many=True
    )

    class Meta:
        model = Participation
        fields = [
            "id",
            "user",
            "assessment_id",
            "role_id",
            "consent",
            "is_profiling_questions_completed",
            "is_pillar_questions_completed",
            "profile_ids",
        ]
        read_only_fields = ["is_profiling_questions_completed"]


class ClosedWithScaleCategoryResponseSerializer(serializers.ModelSerializer):
    participation_response_id = serializers.PrimaryKeyRelatedField(
        source="participation_response",
        queryset=ParticipationResponse.objects.all(),
        required=False,
        allow_null=True,
    )
    assessment_response_id = serializers.PrimaryKeyRelatedField(
        source="assessment_response",
        queryset=AssessmentResponse.objects.all(),
        required=False,
        allow_null=True,
    )
    category_id = serializers.PrimaryKeyRelatedField(
        source="category",
        queryset=Category.objects.all(),
        required=False,
    )
    response_choice_id = serializers.PrimaryKeyRelatedField(
        source="response_choice",
        queryset=ResponseChoice.objects.all(),
        required=True,
        allow_null=True,
    )

    class Meta:
        model = ClosedWithScaleCategoryResponse
        fields = [
            "id",
            "participation_response_id",
            "assessment_response_id",
            "category_id",
            "response_choice_id",
        ]
        optional_fields = [
            "participation_response_id",
            "assessment_response_id",
            "category_id",
        ]


class ResponseSerializer(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(
        source="question", queryset=Question.objects.all()
    )
    unique_choice_response_id = serializers.PrimaryKeyRelatedField(
        source="unique_choice_response",
        queryset=ResponseChoice.objects.all(),
        required=False,
        allow_null=True,
    )
    multiple_choice_response_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        source="multiple_choice_response",
        queryset=ResponseChoice.objects.all(),
        required=False,
    )
    closed_with_scale_response_categories = ClosedWithScaleCategoryResponseSerializer(
        many=True, required=False
    )

    def create(self, validated_data):
        closed_with_scale_response_categories_data = []
        if "closed_with_scale_response_categories" in validated_data.keys():
            closed_with_scale_response_categories_data = validated_data.pop(
                "closed_with_scale_response_categories"
            )
        response = super().create(validated_data)
        for item in closed_with_scale_response_categories_data:
            participation_response = (
                response if response.__class__ == ParticipationResponse else None
            )
            assessment_response = (
                response if response.__class__ == AssessmentResponse else None
            )
            ClosedWithScaleCategoryResponse.objects.create(
                category=item["category"],
                response_choice=item["response_choice"],
                participation_response=participation_response,
                assessment_response=assessment_response,
            )
        return response

    def update(self, instance, validated_data):
        closed_with_scale_response_categories_data = []
        if "closed_with_scale_response_categories" in validated_data.keys():
            closed_with_scale_response_categories_data = validated_data.pop(
                "closed_with_scale_response_categories"
            )
        response = super().update(instance, validated_data)
        for item in closed_with_scale_response_categories_data:
            (
                closedWithScaleCategoryResponse,
                _,
            ) = response.closed_with_scale_response_categories.get_or_create(
                category=item["category"]
            )
            closedWithScaleCategoryResponse.response_choice = item["response_choice"]
            closedWithScaleCategoryResponse.save()
        return response

    class Meta:
        asbtract = True


class ParticipationResponseSerializer(ResponseSerializer):
    participation_id = ParticipationField(source="participation")

    def validate(self, data):
        participation = data["participation"]
        population = participation.assessment.population or 0
        if (
            not Question.objects.filter_by_role(participation.role)
            .filter_by_population(population)
            .filter(id=data["question"].id)
            .exists()
        ):
            raise serializers.ValidationError(
                detail="You don't need to respond to this question.",
                code=ErrorCode.QUESTION_NOT_NEEDED.value,
            )
        question = data["question"]
        if (
            question.objectivity == "objective"
            and question.survey_type == "questionnaire"
        ):
            raise serializers.ValidationError(
                detail="An objective response must be link to the assessment, not the participation",
                code=ErrorCode.NEED_PARTICIPATION_RESPONSE.value,
            )
        return data

    class Meta:
        model = ParticipationResponse
        fields = RESPONSE_FIELDS + ["participation_id"]
        optional_fields = OPTIONAL_RESPONSE_FIELDS
