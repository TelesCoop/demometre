from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from open_democracy_back.factories import QuestionFactory, CriteriaFactory


class TestQuestionnaireViews(TestCase):
    def test_questionnaire_views_query_count(self):
        url = reverse("surveys-all")
        criteria = CriteriaFactory.create()
        for _ in range(20):
            QuestionFactory.create(criteria=criteria)
        with CaptureQueriesContext(connection) as queries:
            self.client.get(url)
        self.assertLessEqual(len(queries), 25)
