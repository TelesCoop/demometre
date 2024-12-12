from django.test import TestCase

from open_democracy_back.factories import (
    SurveyFactory,
    PillarFactory,
    MarkerFactory,
    CriteriaFactory,
    ALL_FACTORY_QUESTION_CLASSES,
)
from open_democracy_back.models import Criteria, Marker, Question
from open_democracy_back.utils import QuestionType, SurveyLocality
from open_democracy_back.views.wagtail_rule_views import (
    duplicate_survey,
    duplicate_question,
)


class TestSurvey(TestCase):
    def test_duplicate_question_works(self):
        criterion = CriteriaFactory.create()
        for FactoryQuestionClass in ALL_FACTORY_QUESTION_CLASSES:
            question = FactoryQuestionClass.create(criteria=criterion)
            question_id = question.id
            duplicated_question = duplicate_question(question, criterion)
            question = Question.objects.get(id=question_id)
            self.assertNotEqual(duplicated_question.id, question.id)
            self.assertEqual(duplicated_question.name, question.name)
            self.assertEqual(duplicated_question.type, question.type)

            if question.type in [
                QuestionType.UNIQUE_CHOICE,
                QuestionType.MULTIPLE_CHOICE,
                QuestionType.CLOSED_WITH_SCALE,
            ]:
                self.assertEqual(
                    duplicated_question.response_choices.count(),
                    question.response_choices.count(),
                )
                self.assertEqual(
                    duplicated_question.response_choices.first().response_choice,
                    question.response_choices.first().response_choice,
                )
                if question.type == QuestionType.CLOSED_WITH_SCALE:
                    self.assertEqual(
                        duplicated_question.categories.count(),
                        question.categories.count(),
                    )
                    self.assertEqual(
                        duplicated_question.categories.first().category_fr,
                        question.categories.first().category_fr,
                    )
            elif question.type == QuestionType.PERCENTAGE:
                self.assertEqual(
                    duplicated_question.percentage_ranges.count(),
                    question.percentage_ranges.count(),
                )
                self.assertEqual(
                    duplicated_question.percentage_ranges.first().lower_bound,
                    question.percentage_ranges.first().lower_bound,
                )
            elif question.type == QuestionType.NUMBER:
                self.assertEqual(
                    duplicated_question.number_ranges.count(),
                    question.number_ranges.count(),
                )
                self.assertEqual(
                    duplicated_question.number_ranges.first().lower_bound,
                    question.number_ranges.first().lower_bound,
                )

    def test_duplicate_survey_works(self):
        survey = SurveyFactory.create()
        child_number = 2
        data = {
            "name": "test",
            "description": "test",
            "survey_locality": SurveyLocality.REGION,
            "code": "R0",
        }

        pillars = PillarFactory.create_batch(child_number, survey=survey)
        for pillar in pillars:
            markers = MarkerFactory.create_batch(child_number, pillar=pillar)

            for marker in markers:
                criteria = CriteriaFactory.create_batch(child_number, marker=marker)
                for criterion in criteria:
                    for FactoryQuestionClass in ALL_FACTORY_QUESTION_CLASSES:
                        FactoryQuestionClass.create(criteria=criterion)

        new_survey = duplicate_survey(data, survey)
        survey.refresh_from_db()
        self.assertNotEqual(new_survey.id, survey.id)
        self.assertEqual(new_survey.name, data["name"])
        self.assertEqual(new_survey.description, data["description"])
        self.assertEqual(new_survey.pillars.count(), survey.pillars.count())
        self.assertEqual(
            Marker.objects.filter(pillar__survey=new_survey).count(),
            Marker.objects.filter(pillar__survey=survey).count(),
        )
        self.assertEqual(
            Marker.objects.filter(pillar__survey=new_survey).first().code,
            Marker.objects.filter(pillar__survey=survey).first().code,
        )
        self.assertEqual(
            Criteria.objects.filter(marker__pillar__survey=new_survey).count(),
            Criteria.objects.filter(marker__pillar__survey=survey).count(),
        )
        self.assertEqual(
            Question.objects.filter(
                criteria__marker__pillar__survey=new_survey
            ).count(),
            Question.objects.filter(criteria__marker__pillar__survey=survey).count(),
        )
