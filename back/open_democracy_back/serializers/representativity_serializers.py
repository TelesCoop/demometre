from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from rest_framework.validators import qs_exists

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


class AssessmentRepresentativityCriteriaRuleSerializer(serializers.ModelSerializer):  # TODO
    """
    """

    assessment_representativity_id = serializers.PrimaryKeyRelatedField(
        queryset=AssessmentRepresentativity.objects.all(),
        source="assessment_representativity"
    )
    response_choice_id = serializers.PrimaryKeyRelatedField(
        queryset=ResponseChoice.objects.filter(representativity_criteria_rule__isnull=False)
        .exclude(
            representativity_criteria_rule__ignore_for_acceptability_threshold=True).exclude(
            representativity_criteria_rule__totally_ignore=True),
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
        assessment_representativity = data[
            "assessment_representativity"] if "assessment_representativity" in data else self.instance.assessment_representativity if self.instance is not None else None
        response_choice = data[
            "response_choice"] if "response_choice" in data else self.instance.response_choice if self.instance is not None else None

        # prevent duplicate
        queryset = AssessmentRepresentativityCriteriaRule.objects.filter(
            assessment_representativity=assessment_representativity, response_choice=response_choice)
        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)

        if "assessment_representativity" in data and "response_choice" in data and qs_exists(queryset):
            message = "The fields assessment_representativity and response_choice must make a unique set."
            raise serializers.ValidationError(message)

        # ensure that response and criteria match
        if assessment_representativity.representativity_criteria.profiling_question_id != \
                response_choice.question_id:
            raise serializers.ValidationError("the response choice does not match the assessment representativity")
        return data
