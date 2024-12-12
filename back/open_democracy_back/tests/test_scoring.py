from statistics import mean

from django.test import TestCase

from open_democracy_back.factories import (
    QuestionFactory,
    ParticipationResponseFactory,
    AssessmentFactory,
    AssessmentResponseFactory,
    ResponseChoiceFactory,
    PercentageRangeFactory,
    CategoryFactory,
    ClosedWithScaleCategoryResponseFactory,
    NumberRangeFactory,
)
from open_democracy_back.models import (
    ParticipationResponse,
    SCORE_MAP,
    AssessmentResponse,
)
from open_democracy_back.scoring import (
    get_score_of_boolean_question,
    get_score_of_unique_choice_question,
    QuestionScore,
    get_score_of_multiple_choice_question,
    get_score_of_percentage_question,
    get_score_of_closed_with_scale_question,
    get_score_of_number_question,
)
from open_democracy_back.utils import QuestionType, QuestionObjectivity


class TestScoring(TestCase):
    def test_participation_response_queryset_works(self):
        question = QuestionFactory(type=QuestionType.BOOLEAN)
        profiling_question = QuestionFactory(
            type=QuestionType.BOOLEAN, profiling_question=True
        )
        assessment = AssessmentFactory()
        bad_responses = [
            # should not count because user is anonymous
            ParticipationResponseFactory(
                boolean_response=True, assessment=assessment, question=question
            ),
            # should not count because it's a profiling question
            ParticipationResponseFactory(
                boolean_response=True,
                assessment=assessment,
                question=profiling_question,
            ),
            # should not count because user has passed this question
            ParticipationResponseFactory(
                assessment=assessment, question=question, has_passed=True
            ),
        ]
        bad_responses[0].participation.user.is_unknown_user = True
        bad_responses[0].participation.user.save()

        valid_response = ParticipationResponseFactory(
            boolean_response=True, assessment=assessment, question=question
        )
        participation_responses = ParticipationResponse.objects.accounted_in_assessment(
            assessment.pk
        )
        self.assertEqual(len(participation_responses), 1)
        self.assertEqual(participation_responses[0].id, valid_response.id)

    def test_assessment_response_queryset_works(self):
        question_1 = QuestionFactory(
            type=QuestionType.BOOLEAN, objectivity=QuestionObjectivity.OBJECTIVE
        )
        question_2 = QuestionFactory(
            type=QuestionType.BOOLEAN, objectivity=QuestionObjectivity.OBJECTIVE
        )
        question_3 = QuestionFactory(
            type=QuestionType.BOOLEAN, objectivity=QuestionObjectivity.OBJECTIVE
        )
        assessment = AssessmentFactory()
        valid_assessment_response = AssessmentResponseFactory(
            boolean_response=True, assessment=assessment, question=question_1
        )
        bad_assessment_responses = [
            # should not count because user has passed this question
            AssessmentResponseFactory(
                has_passed=True, assessment=assessment, question=question_2
            ),
            # should not count because user is anonymous
            AssessmentResponseFactory(
                boolean_response=True, assessment=assessment, question=question_3
            ),
        ]
        bad_assessment_responses[1].answered_by.is_unknown_user = True
        bad_assessment_responses[1].answered_by.save()

        assessment_responses = AssessmentResponse.objects.accounted_in_assessment(
            assessment.pk
        )
        self.assertEqual(len(assessment_responses), 1)
        self.assertEqual(assessment_responses[0].id, valid_assessment_response.id)

    def test_get_score_of_boolean_question_works(self):
        question = QuestionFactory(type=QuestionType.BOOLEAN)
        assessment = AssessmentFactory()
        responses = [
            ParticipationResponseFactory(
                boolean_response=True, assessment=assessment, question=question
            ),
            ParticipationResponseFactory(
                boolean_response=True, assessment=assessment, question=question
            ),
            ParticipationResponseFactory(
                boolean_response=True, assessment=assessment, question=question
            ),
            ParticipationResponseFactory(
                boolean_response=False, assessment=assessment, question=question
            ),
        ]
        average_value = mean([response.boolean_response for response in responses])

        score = get_score_of_boolean_question(
            ParticipationResponse.objects.accounted_in_assessment(assessment.pk)
        )
        self.assertEqual(
            score,
            [
                {
                    "question_id": question.id,
                    "question__criteria_id": question.criteria.id,
                    "question__criteria__marker_id": question.criteria.marker.id,
                    "question__criteria__marker__pillar_id": question.criteria.marker.pillar_id,
                    "avg": average_value,
                    "score": SCORE_MAP[2],
                }
            ],
        )
        responses[0].boolean_response = False
        responses[0].save()
        responses[1].boolean_response = False
        responses[1].save()
        average_value = mean([response.boolean_response for response in responses])

        score = get_score_of_boolean_question(
            ParticipationResponse.objects.accounted_in_assessment(assessment.pk)
        )
        self.assertEqual(len(score), 1)
        self.assertDictEqual(
            score[0],
            {
                "question_id": question.id,
                "question__criteria_id": question.criteria.id,
                "question__criteria__marker_id": question.criteria.marker.id,
                "question__criteria__marker__pillar_id": question.criteria.marker.pillar_id,
                "avg": average_value,
                "score": SCORE_MAP[1],
            },
        )

    def test_get_score_of_unique_choice_question_works(self):
        question = QuestionFactory(type=QuestionType.UNIQUE_CHOICE)
        response_1 = ResponseChoiceFactory(question=question, associated_score=1)
        response_2 = ResponseChoiceFactory(question=question, associated_score=2)
        response_3 = ResponseChoiceFactory(question=question, associated_score=3)
        response_4 = ResponseChoiceFactory(question=question, associated_score=4)
        assessment = AssessmentFactory()
        value = mean(
            [
                response.unique_choice_response.linearized_score
                for response in [
                    ParticipationResponseFactory(
                        unique_choice_response=response_1,
                        assessment=assessment,
                        question=question,
                    ),
                    ParticipationResponseFactory(
                        unique_choice_response=response_2,
                        assessment=assessment,
                        question=question,
                    ),
                    ParticipationResponseFactory(
                        unique_choice_response=response_3,
                        assessment=assessment,
                        question=question,
                    ),
                    ParticipationResponseFactory(
                        unique_choice_response=response_4,
                        assessment=assessment,
                        question=question,
                    ),
                ]
            ]
        )
        participation_responses = ParticipationResponse.objects.accounted_in_assessment(
            assessment.pk
        )
        score = get_score_of_unique_choice_question(participation_responses)

        self.assertEqual(len(score), 1)
        self.assertDictEqual(
            score[0],
            QuestionScore(
                question_id=question.id,
                question__criteria_id=question.criteria.id,
                question__criteria__marker_id=question.criteria.marker.id,
                question__criteria__marker__pillar_id=question.criteria.marker.pillar_id,
                score=value,
            ),
        )

    def test_get_score_of_multiple_choice_question_works(self):
        question = QuestionFactory(type=QuestionType.MULTIPLE_CHOICE)
        response_1 = ResponseChoiceFactory(question=question, associated_score=1)
        response_2 = ResponseChoiceFactory(question=question, associated_score=2)
        response_3 = ResponseChoiceFactory(question=question, associated_score=3)
        response_4 = ResponseChoiceFactory(question=question, associated_score=4)
        assessment = AssessmentFactory()

        ParticipationResponseFactory(
            multiple_choice_response=[response_1],
            assessment=assessment,
            question=question,
        )
        ParticipationResponseFactory(
            multiple_choice_response=[response_2, response_3, response_4],
            assessment=assessment,
            question=question,
        )
        # Take the maximum score of each answer
        value = mean([response_1.linearized_score, response_4.linearized_score])
        participation_responses = ParticipationResponse.objects.accounted_in_assessment(
            assessment.pk
        )
        score = get_score_of_multiple_choice_question(participation_responses)

        self.assertEqual(len(score), 1)
        self.assertDictEqual(
            score[0],
            QuestionScore(
                question_id=question.id,
                question__criteria_id=question.criteria.id,
                question__criteria__marker_id=question.criteria.marker.id,
                question__criteria__marker__pillar_id=question.criteria.marker.pillar_id,
                score=value,
            ),
        )

    def test_get_score_of_percentage_question_works(self):
        question = QuestionFactory(type=QuestionType.PERCENTAGE)
        PercentageRangeFactory(
            question=question, lower_bound=0, upper_bound=30, associated_score=1
        )
        response_percentage_range = PercentageRangeFactory(
            question=question, lower_bound=31, upper_bound=50, associated_score=2
        )
        PercentageRangeFactory(
            question=question, lower_bound=51, upper_bound=100, associated_score=4
        )
        assessment = AssessmentFactory()

        ParticipationResponseFactory(
            percentage_response=20,
            assessment=assessment,
            question=question,
        )
        ParticipationResponseFactory(
            percentage_response=60,
            assessment=assessment,
            question=question,
        )
        participation_responses = ParticipationResponse.objects.accounted_in_assessment(
            assessment.pk
        )
        score = get_score_of_percentage_question(participation_responses)

        self.assertEqual(len(score), 1)
        self.assertDictEqual(
            score[0],
            QuestionScore(
                question_id=question.id,
                question__criteria_id=question.criteria.id,
                question__criteria__marker_id=question.criteria.marker.id,
                question__criteria__marker__pillar_id=question.criteria.marker.pillar_id,
                # Score = 2 because the response is 40 and is in the range [31, 50]
                score=response_percentage_range.linearized_score,
            ),
        )

    def test_get_score_of_closed_with_scale_question_works(self):
        question = QuestionFactory(type=QuestionType.CLOSED_WITH_SCALE)
        response_1 = ResponseChoiceFactory(question=question, associated_score=1)
        response_2 = ResponseChoiceFactory(question=question, associated_score=2)
        response_3 = ResponseChoiceFactory(question=question, associated_score=3)
        response_4 = ResponseChoiceFactory(question=question, associated_score=4)
        category_1 = CategoryFactory(question=question)
        category_2 = CategoryFactory(question=question)
        assessment = AssessmentFactory()

        participation_response_1 = ParticipationResponseFactory(
            assessment=assessment,
            question=question,
        )
        ClosedWithScaleCategoryResponseFactory(
            participation_response=participation_response_1,
            category=category_1,
            response_choice=response_1,
        )
        ClosedWithScaleCategoryResponseFactory(
            participation_response=participation_response_1,
            category=category_2,
            response_choice=response_4,
        )

        participation_response_2 = ParticipationResponseFactory(
            assessment=assessment,
            question=question,
        )
        ClosedWithScaleCategoryResponseFactory(
            participation_response=participation_response_2,
            category=category_1,
            response_choice=response_2,
        )
        ClosedWithScaleCategoryResponseFactory(
            participation_response=participation_response_2,
            category=category_2,
            response_choice=response_3,
        )
        value = mean(
            [
                response_1.linearized_score,
                response_2.linearized_score,
                response_3.linearized_score,
                response_4.linearized_score,
            ]
        )
        participation_responses = ParticipationResponse.objects.accounted_in_assessment(
            assessment.pk
        )
        score = get_score_of_closed_with_scale_question(participation_responses)
        self.assertDictEqual(
            score[0],
            QuestionScore(
                question_id=question.id,
                question__criteria_id=question.criteria.id,
                question__criteria__marker_id=question.criteria.marker.id,
                question__criteria__marker__pillar_id=question.criteria.marker.pillar_id,
                score=value,
            ),
        )

    def test_get_score_of_number_question(self):
        question = QuestionFactory(
            type=QuestionType.NUMBER, max_number_value=100, step_number_value=0.1
        )
        NumberRangeFactory(
            question=question, lower_bound=None, upper_bound=25.5, associated_score=1
        )
        response_range = NumberRangeFactory(
            question=question, lower_bound=25.6, upper_bound=50, associated_score=2
        )
        NumberRangeFactory(
            question=question, lower_bound=50.1, upper_bound=100, associated_score=4
        )
        assessment = AssessmentFactory()

        ParticipationResponseFactory(
            number_response=20.4,
            assessment=assessment,
            question=question,
        )
        ParticipationResponseFactory(
            number_response=60.8,
            assessment=assessment,
            question=question,
        )
        participation_responses = ParticipationResponse.objects.accounted_in_assessment(
            assessment.pk
        )
        score = get_score_of_number_question(participation_responses)

        self.assertEqual(len(score), 1)
        self.assertDictEqual(
            score[0],
            QuestionScore(
                question_id=question.id,
                question__criteria_id=question.criteria.id,
                question__criteria__marker_id=question.criteria.marker.id,
                question__criteria__marker__pillar_id=question.criteria.marker.pillar_id,
                score=response_range.linearized_score,
            ),
        )
