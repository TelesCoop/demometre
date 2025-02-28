from django.test import TestCase
from django.urls import reverse

from open_democracy_back.factories.factories import (
    AssessmentRepresentativityCriteriaRuleFactory,
    ResponseChoiceFactory,
    ParticipationResponseFactory,
    AssessmentFactory,
    RepresentativityCriteriaFactory,
    RepresentativityCriteriaRuleFactory,
)
from open_democracy_back.tests.utils import authenticate


class TestRepresentativityAssessmentResponse(TestCase):
    def test_criteria_rule_applied(self):
        criteriaRule = AssessmentRepresentativityCriteriaRuleFactory.create(
            acceptability_threshold=25,
            assessment_representativity__representativity_criteria__min_rate=40,
        )
        assessment_representativity = criteriaRule.assessment_representativity
        assessment = assessment_representativity.assessment
        criteria = criteriaRule.response_choice.question.representativity_criteria
        other_possible_response = ResponseChoiceFactory.create(
            question=criteria.profiling_question
        )

        # Create responses, one with special rate response and two of one other
        ParticipationResponseFactory.create(
            assessment=assessment,
            question=criteria.profiling_question,
            unique_choice_response=criteriaRule.response_choice,
        )  # 33%

        ParticipationResponseFactory.create(
            assessment=assessment,
            question=criteria.profiling_question,
            unique_choice_response=other_possible_response,
        )
        ParticipationResponseFactory.create(
            assessment=assessment,
            question=criteria.profiling_question,
            unique_choice_response=other_possible_response,
        )  # 66%

        self.assertTrue(assessment_representativity.respected)

    def test_criteria_rule_not_applied_if_ignored(self):
        assessment_criteria_rule = AssessmentRepresentativityCriteriaRuleFactory.create(
            acceptability_threshold=60,  # too high if it were not ignored
            assessment_representativity__representativity_criteria__min_rate=40,
        )
        RepresentativityCriteriaRuleFactory.create(
            representativity_criteria=assessment_criteria_rule.assessment_representativity.representativity_criteria,
            response_choice=assessment_criteria_rule.response_choice,
            ignore_for_acceptability_threshold=True,
        )
        assessment_representativity = (
            assessment_criteria_rule.assessment_representativity
        )
        assessment = assessment_representativity.assessment
        criteria = (
            assessment_criteria_rule.response_choice.question.representativity_criteria
        )
        other_possible_response = ResponseChoiceFactory.create(
            question=criteria.profiling_question
        )

        # Create responses, one with special rate response and two of one other
        ParticipationResponseFactory.create(
            assessment=assessment,
            question=criteria.profiling_question,
            unique_choice_response=assessment_criteria_rule.response_choice,
        )  # 50%

        ParticipationResponseFactory.create(
            assessment=assessment,
            question=criteria.profiling_question,
            unique_choice_response=other_possible_response,
        )  # 50%

        self.assertTrue(assessment_representativity.respected)

    @authenticate
    def test_custom_rates_are_sent(self):
        min_rate = 40
        test_custom_rates_are_sent = 25
        # things are often created manually because creations in save conflict with factories otherwhise
        assessment = AssessmentFactory.create(initiated_by_user=authenticate.user)
        RepresentativityCriteriaFactory.create(min_rate=min_rate)
        assessment_representativity = assessment.representativities.first()
        criteriaRule = AssessmentRepresentativityCriteriaRuleFactory.create(
            acceptability_threshold=test_custom_rates_are_sent,
            assessment_representativity=assessment_representativity,
        )
        ResponseChoiceFactory.create(
            question=assessment_representativity.representativity_criteria.profiling_question
        )

        #
        url = reverse("assessments-detail", args=[assessment.pk])
        res = self.client.get(
            url,
            content_type="application/json",
        )
        representativity = res.json()["representativities"][0]
        self.assertEqual(representativity["minRate"], min_rate)
        self.assertEqual(
            [
                count["acceptabilityThreshold"]
                for count in representativity["countByResponseChoice"]
            ],
            [test_custom_rates_are_sent, None],
        )
        self.assertEqual(
            [count["ruleId"] for count in representativity["countByResponseChoice"]],
            [criteriaRule.id, None],
        )
