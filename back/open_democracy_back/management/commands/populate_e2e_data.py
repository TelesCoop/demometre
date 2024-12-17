import collections

from django.core.management import BaseCommand

from my_auth.models import User
from open_democracy_back.factories import (
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
)
from open_democracy_back.utils import QuestionType


class Command(BaseCommand):
    help = "Command to populate the database for e2e tests"

    def __init__(self):
        super().__init__()
        self.code_per_criteria = collections.Counter()
        self.scores = [1, 2, 3, 4]

    def create_users(self):
        UserFactory.create(email="user@telescoop.fr")

    def create_question(self, criteria, question_type):
        self.code_per_criteria[criteria] += 1
        code = self.code_per_criteria[criteria]
        question = QuestionFactory.create(
            type=question_type,
            criteria=criteria,
            code=code,
            name_fr=f"Question {code} {question_type}",
            question_statement_fr=f"Question {code} statement",
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
        representation, _ = Pillar.objects.get_or_create(name="Représentation")
        Pillar.objects.get_or_create(name="Transparence")
        Pillar.objects.get_or_create(name="Participation")
        Pillar.objects.get_or_create(name="Coopération")

        marker = MarkerFactory.create(pillar=representation, code="1")

        criteria = CriteriaFactory.create(marker=marker, code="1")

        self.create_question(criteria, QuestionType.UNIQUE_CHOICE)
        self.create_question(criteria, QuestionType.MULTIPLE_CHOICE)
        self.create_question(criteria, QuestionType.CLOSED_WITH_SCALE)
        self.create_question(criteria, QuestionType.BOOLEAN)
        self.create_question(criteria, QuestionType.PERCENTAGE)
        self.create_question(criteria, QuestionType.NUMBER)

    def create_locales(self):
        pass

    def handle(self, *args, **options):
        self.create_locales()
        self.create_users()
        self.create_questionnaire()
        n_questions = QuestionnaireQuestion.objects.count()
        n_users = User.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Data populated successfully, {n_questions} questions and {n_users} users in the DB."
            )
        )
