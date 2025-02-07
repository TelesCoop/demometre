from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from open_democracy_back.models import ResponseChoice
from open_democracy_back.models.representativity_models import (
    AssessmentRepresentativity,
    RepresentativityCriteria,
    AssessmentRepresentativityCriteriaRule,
)
from open_democracy_back.serializers_utils import TranslatedField


class AssessmentRepresentativityCriteriaSerializer(serializers.ModelSerializer):
    """
    Count by response choice for all representativity criteria link to a specific assessment
    Need "assessment_id" in context arg
    """

    assessment_id = serializers.PrimaryKeyRelatedField(
        read_only=True, source="assessment"
    )
    representativity_criteria_name = TranslatedField(
        source="representativity_criteria.name"
    )

    min_rate = ReadOnlyField(source="representativity_criteria.min_rate")

    class Meta:
        model = AssessmentRepresentativity
        fields = [
            "id",
            "assessment_id",
            "representativity_criteria_name",
            "count_by_response_choice",
            "min_rate",
            "respected",
        ]
        read_only_fields = fields


class RepresentativityCriteriaSerializer(serializers.ModelSerializer):
    profiling_question_id = serializers.PrimaryKeyRelatedField(
        read_only=True, source="profiling_question"
    )

    class Meta:
        model = RepresentativityCriteria
        fields = [
            "id",
            "survey_locality",
            "name",
            "profiling_question_id",
            "min_rate",
            "explanation",
        ]
        read_only_fields = fields


class AssessmentRepresentativityCriteriaRuleSerializer(serializers.ModelSerializer):
    """
    """

    assessment_representativity_id = serializers.PrimaryKeyRelatedField(
        queryset=AssessmentRepresentativity.objects.all(),  # really have all?
        source="assessment_representativity"
    )
    response_choice_id = serializers.PrimaryKeyRelatedField(
        queryset=ResponseChoice.objects.all(),  # really have all?
        source="response_choice"
    )

    class Meta:
        model = AssessmentRepresentativityCriteriaRule
        fields = [
            "id",
            "assessment_id",
            "assessment_representativity_id",
            "response_choice_id",
            "acceptability_threshold"
        ]

    def validate(self, data):
        if data["assessment_representativity"].representativity_criteria.profiling_question_id != data["response_choice"].question_id:
            raise serializers.ValidationError("the response choice does not match the assessment representativity")
        return data
