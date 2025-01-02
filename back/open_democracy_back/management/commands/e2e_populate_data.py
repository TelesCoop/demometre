import collections
import os

from django.contrib.auth.models import Group
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
    ProfileType,
    ProfileDefinition,
    Question,
    RepresentativityCriteria,
    AssessmentType,
)
from open_democracy_back.utils import (
    QuestionType,
    SurveyLocality,
    QuestionObjectivity,
    ManagedAssessmentType,
)


class Command(BaseCommand):
    help = "Command to populate the database for e2e tests"

    def __init__(self):
        super().__init__()
        self.code_per_criteria = collections.Counter()
        self.scores = [1, 2, 3, 4]

    def handle(self, *args, **options):
        if not os.environ.get("E2E_TESTS"):
            raise NotImplementedError("This command is only for e2e tests")

        self.create_locales()
        self.create_users()
        self.create_pages()
        self.create_cities()

        self.create_questionnaire()
        self.create_objective_questions()
        self.create_roles()
        self.create_profiling_questions()
        self.create_profile_types()
        self.create_conditional_questions()
        self.create_representativity_criterias()

        self.create_experts()

        models_to_count = [QuestionnaireQuestion, User, Page]
        count = {}
        for model in models_to_count:
            count[model._meta.verbose_name] = model.objects.count()
        formatted_count = ", ".join([f"{k}: {v} items" for k, v in count.items()])
        self.stdout.write(
            self.style.SUCCESS(f"Data populated successfully, {formatted_count}")
        )

    def create_users(self):
        for i in range(5):
            UserFactory.create(
                email=f"user{i+1}@telescoop.fr",
            )
        UserFactory.create(
            email="superuser@telescoop.fr",
            is_staff=True,
            is_superuser=True,
        )

    def create_profile_types(self):
        profile_type_1, _ = ProfileType.objects.update_or_create(
            name="Profile 1-1",
            defaults=dict(name_fr="Profile 1-1", rules_intersection_operator="and"),
        )
        question = Question.objects.get(code="Profile-1")
        definition, _ = ProfileDefinition.objects.update_or_create(
            profile_type=profile_type_1,
            defaults=dict(
                conditional_question=question,
            ),
        )
        definition.response_choices.set(
            ResponseChoice.objects.filter(question=question, associated_score=1)
        )

        profile_type_2, _ = ProfileType.objects.update_or_create(
            name="Profile 2-high",
            defaults=dict(name_fr="Profile 2-high", rules_intersection_operator="and"),
        )
        question = Question.objects.get(code="Profile-2")
        definition, _ = ProfileDefinition.objects.update_or_create(
            profile_type=profile_type_2,
            defaults=dict(
                conditional_question=question,
                numerical_operator=">",
                float_value=30,
            ),
        )
        definition.response_choices.set(
            ResponseChoice.objects.filter(question=question, associated_score=1)
        )

    def create_conditional_questions(self):
        marker = MarkerFactory.create(
            pillar=Pillar.objects.get_or_create(name="transparence")[0],
            code="1",
            name="Marker T.1",
        )
        criteria = CriteriaFactory.create(
            marker=marker, code="1", name="Criteria T.1.1"
        )

        question = self.create_question(criteria, QuestionType.UNIQUE_CHOICE)
        question.profiles.add(ProfileType.objects.get(name="Profile 1-1"))
        question = self.create_question(criteria, QuestionType.MULTIPLE_CHOICE)
        question.profiles.add(ProfileType.objects.get(name="Profile 2-high"))

        question = self.create_question(criteria, QuestionType.BOOLEAN)
        question.roles.set([Role.objects.get(name="Élu")])

    def create_profiling_questions(self):
        surveys = Survey.objects.all()
        question = self.create_question(
            None,
            QuestionType.UNIQUE_CHOICE,
            profiling_question=True,
            code="Profile-1",
            n_choices=3,
        )
        question.surveys.set(surveys)
        question = self.create_question(
            None, QuestionType.NUMBER, profiling_question=True, code="Profile-2"
        )
        question.surveys.set(surveys)

    def create_question(
        self,
        criteria,
        question_type,
        profiling_question=False,
        code=None,
        statement=None,
        objective=False,
        n_choices=None,
    ):
        self.code_per_criteria[criteria] += 1
        if code is None:
            code = self.code_per_criteria[criteria]
        statement_prefix = "Profiling " if profiling_question else ""
        question_statement = (
            statement or f"{statement_prefix}Question {code} {question_type} statement"
        )
        objectivity = (
            QuestionObjectivity.OBJECTIVE
            if objective
            else QuestionObjectivity.SUBJECTIVE
        )

        question = QuestionFactory.create(
            type=question_type,
            criteria=criteria,
            code=code,
            name_fr=f"Question {code} {question_type}",
            question_statement_fr=question_statement,
            profiling_question=profiling_question,
            objectivity=objectivity,
        )
        if question_type in [
            QuestionType.UNIQUE_CHOICE,
            QuestionType.MULTIPLE_CHOICE,
            QuestionType.CLOSED_WITH_SCALE,
        ]:
            n_choices = n_choices or 4
            for choice, score in zip(range(1, n_choices + 1), self.scores):
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
        return question

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

        marker = MarkerFactory.create(
            pillar=representation, code="1", name="Marker R.1"
        )

        criteria = CriteriaFactory.create(
            marker=marker, code="1", name="Criteria R.1.1"
        )

        self.create_question(criteria, QuestionType.UNIQUE_CHOICE)
        self.create_question(criteria, QuestionType.MULTIPLE_CHOICE)
        self.create_question(criteria, QuestionType.CLOSED_WITH_SCALE)
        self.create_question(criteria, QuestionType.BOOLEAN)
        self.create_question(criteria, QuestionType.PERCENTAGE)
        self.create_question(criteria, QuestionType.NUMBER)

        for pillar in Pillar.objects.all():
            pillar.save()

        AssessmentType.objects.update_or_create(
            assessment_type=ManagedAssessmentType.QUICK,
            defaults=dict(publish_results_regardless_of_representativities=True),
        )

    def create_objective_questions(self):
        pillar = Pillar.objects.get(name="participation", survey__code="M")
        marker = MarkerFactory.create(pillar=pillar, code="1", name="Marker P.1")
        criteria = CriteriaFactory.create(
            marker=marker, code="1", name="Criteria P.1.1"
        )
        self.create_question(
            criteria,
            QuestionType.NUMBER,
            statement="Nombre de doigts dans une main ?",
            objective=True,
        )

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

        for index in range(1, 6):
            code = f"9990{index}"
            epci, _ = EPCI.objects.get_or_create(
                code=code, defaults=dict(name=f"EPCI test {index}")
            )
            municipality, _ = Municipality.objects.update_or_create(
                code=code,
                defaults=dict(
                    name=f"Ville test {index}", population=1000, department=departement
                ),
            )
            MunicipalityOrderByEPCI.objects.get_or_create(
                epci=epci, municipality=municipality
            )
            ZipCode.objects.get_or_create(
                code=code, defaults=dict(municipality=municipality)
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

    def create_representativity_criterias(self):
        repr_criteria, _ = RepresentativityCriteria.objects.update_or_create(
            name="Représentativité 1",
            defaults=dict(
                survey_locality=SurveyLocality.CITY,
                profiling_question=Question.objects.get(code="Profile-1"),
                min_rate=25,
                name_fr="Représentativité 1",
                explanation_fr="Représentativité 1 explication",
            ),
        )

    def create_experts(self):
        group, _ = Group.objects.get_or_create(name="Experts")
        user = UserFactory.create(
            email="expert@telescoop.fr", first_name="Expert", last_name="1"
        )
        user.groups.set([group])
