from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from open_democracy_back.factories.factories import (
    AssessmentFactory,
    AssessmentTypeFactory,
)


class TestPerformance(TestCase):

    def test_assessment_published(self):
        AssessmentTypeFactory.create(
            publish_results_regardless_of_representativities=True
        )
        AssessmentFactory.create_batch(10)

        url = reverse("assessments-published")

        # Is was 111 before. This is still too much :/
        with self.assertNumQueries(45):
            res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 10)
