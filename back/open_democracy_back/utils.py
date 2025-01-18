from django.db import models
from django.utils.translation import gettext_lazy as _


EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

SIMPLE_RICH_TEXT_FIELD_FEATURE = [
    "bold",
    "italic",
    "link",
    "ol",
    "ul",
]

NUMERICAL_OPERATOR = [
    ("<", "<"),
    (">", ">"),
    ("<=", "<="),
    (">=", ">="),
    ("!=", "!="),
    ("=", "="),
]


# NB : use get_<field_name>_display() to retrieve the second argument of TextChoices
class LocalityType(models.TextChoices):
    MUNICIPALITY = "municipality", _("Commune")
    INTERCOMMUNALITY = "intercommunality", _("Intercommunalité")
    DEPARTMENT = "department", _("Département")
    REGION = "region", _("Région")


class InitiatorType(models.TextChoices):
    COLLECTIVITY = "collectivity", _("La collectivité")
    ASSOCIATION = "association", _("Une association")
    INDIVIDUAL = "individual", _("Un particulier")
    OTHER = "other", _("Autre")


class ManagedAssessmentType(models.TextChoices):
    QUICK = "quick", _("Diagnostic rapide")
    PARTICIPATIVE = "participative", _("Evaluation participative")
    WITH_EXPERT = "with_expert", _("Evaluation avec expert")


class BooleanOperator(models.TextChoices):
    AND = "and", _("et")
    OR = "or", _("ou")


class QuestionType(models.TextChoices):
    UNIQUE_CHOICE = "unique_choice", _("Choix unique")
    MULTIPLE_CHOICE = "multiple_choice", _("Choix multiple")
    CLOSED_WITH_SCALE = "closed_with_scale", _("Fermée à échelle")
    BOOLEAN = "boolean", _("Binaire oui / non")
    PERCENTAGE = "percentage", _("Pourcentage")
    NUMBER = "number", _("Nombre")


class QuestionObjectivity(models.TextChoices):
    OBJECTIVE = "objective", _("Objective")
    SUBJECTIVE = "subjective", _("Subjective")


class QuestionMethod(models.TextChoices):
    QUANTITATIVE = "quantitative", _("Quantitative")
    QUALITATIVE = "qualitative", _("Qualitative")


QUESTION_TYPE_WITH_SCORE = [
    QuestionType.BOOLEAN,
    QuestionType.UNIQUE_CHOICE,
    QuestionType.MULTIPLE_CHOICE,
    QuestionType.PERCENTAGE,
    QuestionType.NUMBER,
    QuestionType.CLOSED_WITH_SCALE,
]


class SerializerContext:
    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {"request": self.request, "format": self.format_kwarg, "view": self}


def generate_randon_string_char_and_digits(length):
    import random
    import string

    letters_and_digits = string.ascii_letters + string.digits
    result_str = "".join(random.choice(letters_and_digits) for i in range(length))
    return result_str


class PillarName(models.TextChoices):
    REPRESENTATION = "représentation", _("Représentation")
    TRANSPARENCY = "transparence", _("Transparence")
    PARTICIPATION = "participation", _("Participation")
    COOPERATION = "coopération", _("Coopération")


class SurveyLocality(models.TextChoices):
    CITY = "city", _("Commune/EPCI")
    DEPARTMENT = "department", _("Département")
    REGION = "region", _("Région")
