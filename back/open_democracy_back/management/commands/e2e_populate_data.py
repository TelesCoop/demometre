import collections

from django.core.management import BaseCommand
from wagtail.models import Locale, Page

import open_democracy_back.models as democracy_models
from my_auth.models import User
from open_democracy_back.factories import page_factories
from open_democracy_back.factories.factories import (
    MarkerFactory,
    CriteriaFactory,
    QuestionFactory,
    UserFactory,
)
from open_democracy_back.models import (
    Pillar,
    QuestionnaireQuestion,
    ResponseChoice,
    Category,
    PercentageRange,
    NumberRange,
    Survey,
    Department,
    Region,
    EPCI,
    Municipality,
    MunicipalityOrderByEPCI,
    ZipCode,
    Role,
)
from open_democracy_back.utils import QuestionType, SurveyLocality


class Command(BaseCommand):
    help = "Command to populate the database for e2e tests"

    def __init__(self):
        super().__init__()
        self.code_per_criteria = collections.Counter()
        self.scores = [1, 2, 3, 4]

    def create_users(self):
        UserFactory.create(
            email="user@telescoop.fr",
        )
        UserFactory.create(
            email="superuser@telescoop.fr",
            is_staff=True,
            is_superuser=True,
        )

    def create_profile_types(self):
        pass

    def create_profiling_questions(self):
        self.create_question(None, QuestionType.UNIQUE_CHOICE, profiling_question=True)
        self.create_question(None, QuestionType.NUMBER, profiling_question=True)

    def create_question(self, criteria, question_type, profiling_question=False):
        self.code_per_criteria[criteria] += 1
        code = self.code_per_criteria[criteria]
        question = QuestionFactory.create(
            type=question_type,
            criteria=criteria,
            code=code,
            name_fr=f"Question {code} {question_type}",
            question_statement_fr=f"Question {code} statement",
            profiling_question=profiling_question,
        )
        if question_type in [
            QuestionType.UNIQUE_CHOICE,
            QuestionType.MULTIPLE_CHOICE,
            QuestionType.CLOSED_WITH_SCALE,
        ]:
            for choice, score in zip(range(1, 5), self.scores):
                ResponseChoice.objects.get_or_create(
                    question=question,
                    response_choice_fr=f"choice {choice}",
                    associated_score=score,
                )
        if question_type == QuestionType.CLOSED_WITH_SCALE:
            for category_ix in range(1, 3):
                Category.objects.get_or_create(
                    question=question,
                    category_fr=f"Catégorie {category_ix}",
                )
        if question_type == QuestionType.PERCENTAGE:
            bounds_list = [(0, 24), (25, 49), (50, 74), (75, 100)]
            for bounds, score in zip(bounds_list, self.scores):
                PercentageRange.objects.get_or_create(
                    question=question,
                    associated_score=score,
                    defaults=dict(
                        lower_bound=bounds[0],
                        upper_bound=bounds[1],
                    ),
                )
        if question_type == QuestionType.NUMBER:
            bounds_list = [(0, 10), (11, 20), (21, 30), (31, 40)]
            for bounds, score in zip(bounds_list, self.scores):
                NumberRange.objects.get_or_create(
                    question=question,
                    associated_score=score,
                    defaults=dict(
                        lower_bound=bounds[0],
                        upper_bound=bounds[1],
                    ),
                )

    def create_questionnaire(self):
        survey, _ = Survey.objects.update_or_create(
            survey_locality=SurveyLocality.CITY, defaults=dict(code="M")
        )
        representation, _ = Pillar.objects.get_or_create(
            name="représentation", defaults=dict(survey=survey)
        )
        Pillar.objects.get_or_create(name="transparence", defaults=dict(survey=survey))
        Pillar.objects.get_or_create(name="participation", defaults=dict(survey=survey))
        Pillar.objects.get_or_create(name="coopération", defaults=dict(survey=survey))

        marker = MarkerFactory.create(pillar=representation, code="1")

        criteria = CriteriaFactory.create(marker=marker, code="1")

        self.create_question(criteria, QuestionType.UNIQUE_CHOICE)
        self.create_question(criteria, QuestionType.MULTIPLE_CHOICE)
        self.create_question(criteria, QuestionType.CLOSED_WITH_SCALE)
        self.create_question(criteria, QuestionType.BOOLEAN)
        self.create_question(criteria, QuestionType.PERCENTAGE)
        self.create_question(criteria, QuestionType.NUMBER)

        for pillar in Pillar.objects.all():
            pillar.save()

    @staticmethod
    def create_locales():
        Locale.objects.get_or_create(language_code="fr")
        Locale.objects.get_or_create(language_code="en")

    @staticmethod
    def set_custom_data_for_usage_page():
        if (
            usage_page := democracy_models.UsagePage.objects.get()
        ).start_assessment_block_data.raw_data:
            return
        usage_page.start_assessment_block_data = [
            {
                "type": "assessment_type",
                "value": {
                    "title": "Diagnostic rapide",
                    "type": "quick",
                    "pdf_button": "Télécharger le diagnostic rapide",
                },
                "id": "4dac6755-0bdf-4354-a7aa-4f7fac116f2f",
            },
            {
                "type": "assessment_type",
                "value": {
                    "title": "L'évaluation participative",
                    "type": "participative",
                    "pdf_button": "Télécharger le questionnaire",
                },
                "id": "81907e1d-430c-4714-9d14-525c911b77b5",
            },
            {
                "type": "assessment_type",
                "value": {
                    "title": "L'évaluation avec experts",
                    "type": "with_expert",
                    "pdf_button": "Guide de l'accompagnateur",
                },
                "id": "684871e0-01dd-4db4-8c07-23f2f4ff2367",
            },
        ]
        usage_page.save()

    def create_pages(self):
        page_models = [
            democracy_models.HomePage,
            democracy_models.UsagePage,
            democracy_models.ReferentialPage,
            democracy_models.ParticipationBoardPage,
            democracy_models.ResultsPage,
            democracy_models.ProjectPage,
            democracy_models.EvaluationInitiationPage,
            democracy_models.EvaluationQuestionnairePage,
            democracy_models.AnimatorPage,
            democracy_models.ContentPage,
        ]
        root = Page.objects.get(pk=1)
        n_added = 0
        for page_model in page_models:
            if page_model.objects.count():
                continue
            instance = getattr(page_factories, f"{page_model.__name__}Factory").build()
            root.add_child(instance=instance)
            n_added += 1

        self.set_custom_data_for_usage_page()
        return n_added

    @staticmethod
    def create_cities():
        region, _ = Region.objects.get_or_create(
            code="999", defaults=dict(name="Région test")
        )
        departement, _ = Department.objects.get_or_create(
            code="999", defaults=dict(name="Département test", region=region)
        )
        epci, _ = EPCI.objects.get_or_create(
            code="99901", defaults=dict(name="EPCI test")
        )
        municipality, _ = Municipality.objects.get_or_create(
            code="99901",
            defaults=dict(name="Ville test", population=1000, department=departement),
        )
        MunicipalityOrderByEPCI.objects.get_or_create(
            epci=epci, municipality=municipality
        )
        ZipCode.objects.get_or_create(
            code="99901", defaults=dict(municipality=municipality)
        )

    @staticmethod
    def create_roles():
        Role.objects.get_or_create(
            name="Citoyen",
            defaults=dict(
                name_fr="Citoyen",
                description="Citoyen",
            ),
        )
        Role.objects.get_or_create(
            name="Élu",
            defaults=dict(
                name_fr="Élu",
                description="Élu",
            ),
        )
        Role.objects.get_or_create(
            name="Autre rôle",
            defaults=dict(
                name_fr="Autre rôle",
                description="Autre rôle",
            ),
        )

    def handle(self, *args, **options):
        self.create_locales()
        self.create_users()
        self.create_questionnaire()
        self.create_pages()
        self.create_cities()
        self.create_roles()
        n_questions = QuestionnaireQuestion.objects.count()
        n_users = User.objects.count()
        n_pages = Page.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Data populated successfully, {n_questions} questions {n_users} users and {n_pages} pages in the DB."
            )
        )
