from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from open_democracy_back.factories.factories import (
    QuestionFactory,
    CriteriaFactory,
    AssessmentFactory,
    ParticipationFactory,
    ResponseChoiceFactory,
)
from open_democracy_back.models import ParticipativeProcess, ParticipationResponse
from open_democracy_back.tests.utils import authenticate


class TestQuestionnaireViews(TestCase):
    def test_questionnaire_views_query_count(self):
        url = reverse("surveys-all")
        criteria = CriteriaFactory.create()
        for _ in range(20):
            QuestionFactory.create(criteria=criteria)
        with CaptureQueriesContext(connection) as queries:
            self.client.get(url)
        self.assertLessEqual(len(queries), 25)

    @authenticate
    def test_can_add_participative_processes_to_a_participation(self) -> object:
        ass = AssessmentFactory.create()
        ParticipationFactory.create(user=authenticate.user, assessment=ass)
        r1 = ResponseChoiceFactory.create()
        pp = ParticipativeProcess.objects.create(
            assessment=ass, response_choice=r1, name="PP 1"
        )
        url = reverse("Participation-list")
        res = self.client.post(
            url,
            {"participativeProcesses": [pp.pk], "assessmentId": ass.pk},
            content_type="application/json",
        )
        self.assertListEqual(res.data["participative_processes"], [pp.pk])

    @authenticate
    def test_reponse_with_participative_process(self) -> object:
        url = reverse("ParticipationResponse-list")
        question = QuestionFactory.create(is_participative_process_question=True)
        ass = AssessmentFactory.create()
        participation = ParticipationFactory.create(
            user=authenticate.user, assessment=ass
        )
        rp = ResponseChoiceFactory.create()
        pp1 = ParticipativeProcess.objects.create(
            response_choice=rp, assessment=ass, name="name"
        )
        pp2 = ParticipativeProcess.objects.create(
            response_choice=rp, assessment=ass, name="name"
        )

        # can answer with a participative process
        res = self.client.post(
            url,
            {
                "question_id": question.pk,
                "boolean_response": False,
                "participation_id": participation.pk,
                "participative_process_id": pp1.pk,
            },
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        participation_response = ParticipationResponse.objects.get()

        # can answer for another participative process
        res = self.client.post(
            url,
            {
                "question_id": question.pk,
                "booleanReponse": False,
                "participation_id": participation.pk,
                "participative_process_id": pp2.pk,
            },
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)

        # can answer without a participative process
        res = self.client.post(
            url,
            {
                "question_id": question.pk,
                "booleanReponse": False,
                "participation_id": participation.pk,
                "participative_process_id": None,
            },
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)

        # when answering for same participative process, we do not create another object
        res = self.client.post(
            url,
            {
                "question_id": question.pk,
                "booleanReponse": False,
                "participation_id": participation.pk,
                "participative_process_id": pp1.pk,
            },
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["id"], participation_response.pk)
