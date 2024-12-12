import datetime
import os

from django.conf import settings
from django.contrib.auth.models import Group
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from open_democracy_back.factories import (
    AssessmentFactory,
    ParticipationFactory,
    UserFactory,
    MunicipalityFactory,
    AssessmentTypeFactory,
    SurveyFactory,
)
from open_democracy_back.models import Assessment
from open_democracy_back.tests.utils import authenticate
from open_democracy_back.utils import ManagedAssessmentType


class TestScoring(TestCase):
    def get_role(self, assessment: Assessment):
        url = reverse("assessments-detail", args=[assessment.pk])
        return self.client.get(url).data["details"]["role"]

    @authenticate
    def test_assessment_role(self):
        assessment = AssessmentFactory.create()
        self.assertEqual(self.get_role(assessment), "")
        ParticipationFactory.create(assessment=assessment, user=authenticate.user)
        self.assertEqual(self.get_role(assessment), "participant")
        assessment.experts.add(authenticate.user)
        self.assertEqual(self.get_role(assessment), "expert")
        assessment.initiated_by_user = authenticate.user
        assessment.save()
        self.assertEqual(self.get_role(assessment), "initiator")


class TestAssessmentsEdits(TestCase):
    @authenticate
    def test_assessment_edits(self):
        assessment = AssessmentFactory.create()
        url = reverse("assessments-detail", args=[assessment.pk])
        res = self.client.patch(
            url,
            {"context": "new context"},
            content_type="application/json",
        )
        # we don't have write access to this assessment
        self.assertEqual(res.status_code, 403)
        assessment.initiated_by_user = authenticate.user
        assessment.save()
        res = self.client.patch(
            url,
            {"context": "new context"},
            content_type="application/json",
        )
        # now it's fine
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["context"], "new context")

    @authenticate
    def test_upload_and_edit_assessment_document(self):
        assessment = AssessmentFactory.create(initiated_by_user=authenticate.user)
        url = reverse("assessment-documents-list")

        # upload document
        with open(
            os.path.join(
                settings.BASE_DIR, "open_democracy_back", "tests", "document.pdf"
            ),
            "rb",
        ) as fh:
            data = self.client.post(
                url,
                {
                    "category": "invoices",
                    "name": "my name",
                    "file": fh,
                    "assessment": assessment.pk,
                },
            ).json()
        self.assertDictEqual(
            {
                "assessment": assessment.pk,
                "category": "invoices",
                "name": "my name",
            },
            {k: v for k, v in data.items() if k in ["assessment", "category", "name"]},
        )

        # test editing document name
        document_pk = data["id"]
        url = reverse("assessment-documents-detail", args=[document_pk])
        data = self.client.patch(
            url,
            {"name": "modified name"},
            content_type="application/json",
        ).json()
        self.assertEqual(data["name"], "modified name")

        # test editing does not work when no right access
        assessment.initiated_by_user = UserFactory.create()
        assessment.save()
        res = self.client.patch(url, {"name": "0"}, content_type="application/json")
        self.assertEqual(res.status_code, 403)

    @authenticate
    def test_assessment_detail_access(self):
        # has detail access
        assessment = AssessmentFactory.create(initiated_by_user=authenticate.user)
        url = reverse("assessments-detail", args=[assessment.pk])
        data = self.client.get(url).json()
        self.assertEqual(data["details"]["hasDetailAccess"], True)
        self.assertEqual(data["context"], assessment.context)

        # no detail access
        assessment.initiated_by_user = UserFactory.create()
        assessment.save()
        data = self.client.get(url).json()
        self.assertEqual(data["details"]["hasDetailAccess"], False)
        self.assertFalse("context" in data)

    @authenticate
    def test_assessments_mine(self):
        """
        Test assessments/mine returns assessments I participated in, for which I'm
        expert and that I initiated.
        """
        url = reverse("assessments-mine")
        pks = set()
        pks.add(AssessmentFactory.create(initiated_by_user=authenticate.user).pk)
        assessment = AssessmentFactory.create()
        assessment.experts.add(authenticate.user)
        pks.add(assessment.pk)
        assessment = AssessmentFactory.create()
        ParticipationFactory.create(user=authenticate.user, assessment=assessment)
        pks.add(assessment.pk)
        # user has no link to this assessment, it should not appear in pks
        AssessmentFactory.create()
        pks_mine = {assessment["id"] for assessment in self.client.get(url).json()}
        self.assertSetEqual(pks, pks_mine)

    @authenticate
    def test_experts(self):
        assessment = AssessmentFactory.create(initiated_by_user=authenticate.user)
        url = reverse("assessments-detail", args=[assessment.pk])
        experts_url = reverse("experts-list")

        self.assertListEqual(self.client.get(experts_url).json(), [])

        # create an expert
        expert = UserFactory.create()
        experts_group, _ = Group.objects.get_or_create(name="Experts")
        expert.groups.add(experts_group)
        # check it's listed as expert
        self.assertEqual(len(self.client.get(experts_url).json()), 1)

        # add it to the statement with a patch
        self.assertEqual(
            self.client.patch(
                url,
                {"experts": [expert.pk]},
                content_type="application/json",
            ).json()["experts"],
            [expert.pk],
        )

        # remove it with another patch
        self.assertEqual(
            self.client.patch(
                url,
                {"experts": []},
                content_type="application/json",
            ).json()["experts"],
            [],
        )

    @authenticate
    def test_can_close_assessment_and_closing_sends_mail(self):
        assessment = AssessmentFactory.create(initiated_by_user=authenticate.user)
        url = reverse("assessments-detail", args=[assessment.pk])
        self.assertEqual(assessment.end_date, None)
        today = datetime.date.today().isoformat()
        res = self.client.patch(
            url,
            {"end_date": today},
            content_type="application/json",
        )
        self.assertEqual(res.json()["endDate"], today)

        # check that the mail was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Cloture d'une évaluation")


class TestAssessmentCreation(TestCase):
    def test_anonymous_can_create_assessment(self):
        municipality = MunicipalityFactory.create()
        SurveyFactory.create()
        url = (
            reverse(
                "create-assessment",
            )
            + f"?locality_id={municipality.pk}&locality_type=municipality"
        )
        res = self.client.get(url)
        assessment_id = res.json()["id"]

        # same request as a new user, make sure we join the same one
        user = UserFactory.create()
        self.client.force_login(user=user)
        res = self.client.get(url)
        self.assertEqual(res.json()["id"], assessment_id)

    @authenticate
    def test_cannot_join_quick_assessment(self):
        """
        When a QUICK assessment is already created by another user for a municipality
        and we get-or-create an assessment for that municipality, a new assessment is
        created.
        """
        SurveyFactory.create()
        municipality = MunicipalityFactory.create()
        assessment = AssessmentFactory.create(
            assessment_type=AssessmentTypeFactory.create(
                assessment_type=ManagedAssessmentType.QUICK
            ),
            municipality=municipality,
        )
        url = (
            reverse(
                "create-assessment",
            )
            + f"?locality_id={municipality.pk}&locality_type=municipality"
        )
        res = self.client.get(url)
        self.assertNotEqual(res.json()["id"], assessment.pk)

    @authenticate
    def test_can_join_participative_and_with_expert_assessment(self):
        """
        When a non-QUICK assessment is already created by another user for a
        municipality and we get-or-create an assessment for that municipality,
        the already created assessment is returned.
        """
        SurveyFactory.create()
        for assessment_type in [
            ManagedAssessmentType.PARTICIPATIVE,
            ManagedAssessmentType.WITH_EXPERT,
        ]:
            municipality = MunicipalityFactory.create()
            assessment = AssessmentFactory.create(
                assessment_type=AssessmentTypeFactory.create(
                    assessment_type=assessment_type
                ),
                municipality=municipality,
            )
            url = (
                reverse(
                    "create-assessment",
                )
                + f"?locality_id={municipality.pk}&locality_type=municipality"
            )
            res = self.client.get(url)
            self.assertEqual(res.json()["id"], assessment.pk)
