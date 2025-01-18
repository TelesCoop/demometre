from django.db import models
from django.db.models import Count, F, Q
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.fields import RichTextField


from open_democracy_back.models.assessment_models import Assessment

from open_democracy_back.models.questionnaire_and_profiling_models import (
    ProfilingQuestion,
    QuestionType,
    ResponseChoice,
)
from open_democracy_back.utils import SIMPLE_RICH_TEXT_FIELD_FEATURE, SurveyLocality


@register_snippet
class RepresentativityCriteria(index.Indexed, models.Model):
    survey_locality = models.CharField(
        max_length=32,
        choices=SurveyLocality.choices,
        default=SurveyLocality.CITY,
        verbose_name=_("Échelon questionnaire"),
    )
    name = models.CharField(max_length=64, verbose_name="Nom")
    profiling_question = models.OneToOneField(
        ProfilingQuestion,
        on_delete=models.CASCADE,
        verbose_name=_("Question de profilage reliée"),
        related_name="representativity_criteria",
        limit_choices_to={"type": QuestionType.UNIQUE_CHOICE},
    )
    min_rate = models.IntegerField(
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name=_(
            "Taux (en %) minimum acceptable pour la publication des résultats"
        ),
        help_text=_(
            "En dessous de ce taux (%) la publication des résultats est interdite"
        ),
    )
    explanation = RichTextField(
        default="",
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Explication"),
        blank=True,
        help_text=_(
            "L'explication doit aider l'utilisateur à savoir quel pourcentage indiquer et expliciter le pourcentage renseigné par défault"
        ),
    )

    search_fields = [
        index.SearchField(
            "name",
        ),
    ]

    panels = [
        FieldPanel("name"),
        FieldPanel("survey_locality"),
        FieldPanel("profiling_question"),
        FieldPanel("min_rate"),
        FieldPanel("explanation"),
    ]

    translated_fields = [
        "name",
        "explanation",
    ]

    def __str__(self):
        locale = translation.get_language()
        return getattr(self, f"name_{locale}")

    def save(self, *args, **kwargs):
        must_create_assessment_representativity = False
        if not self.id:
            must_create_assessment_representativity = True
        super().save(*args, **kwargs)
        if must_create_assessment_representativity:
            for assessment in Assessment.objects.filter(
                survey__survey_locality=self.survey_locality
            ):
                AssessmentRepresentativity.objects.create(
                    assessment=assessment, representativity_criteria_id=self.id
                )

    class Meta:
        verbose_name = _("Critère de représentativité")
        verbose_name_plural = _("Critères de représentativité")


class RepresentativityCriteriaRule(models.Model):
    representativity_criteria = models.ForeignKey(
        RepresentativityCriteria,
        on_delete=models.CASCADE,
        related_name="rules",
    )

    response_choice = models.OneToOneField(
        ResponseChoice,
        on_delete=models.CASCADE,
        verbose_name=_("Réponse"),
        related_name="representativity_criteria_rule",
    )

    ignore_for_acceptability_threshold = models.BooleanField(
        default=False,
        verbose_name=_("Ne pas compter pour le seuil d'acceptabilité minimal"),
        help_text=_("Ex: binaire pour la parité"),
    )
    totally_ignore = models.BooleanField(
        default=False,
        verbose_name=_("Ignorer totalement"),
    )

    def __str__(self):
        return f"{self.representativity_criteria} - {self.response_choice}"

    class Meta:
        unique_together = ["representativity_criteria", "response_choice"]


class AssessmentRepresentativity(models.Model):
    assessment = models.ForeignKey(
        Assessment, on_delete=models.CASCADE, related_name="representativities"
    )
    representativity_criteria = models.ForeignKey(
        RepresentativityCriteria,
        on_delete=models.CASCADE,
        related_name="representativities",
    )
    acceptability_threshold = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name=_("Seuil d'acceptabilité"),
    )

    @property
    def count_by_response_choice(self):
        # annotate() : rename fields
        # values() : specifies which columns are going to be used to "group by"
        # annotate() : specifies an operation over the grouped values
        locale = translation.get_language()
        return (
            self.representativity_criteria.profiling_question.response_choices.all()
            .exclude(representativity_criteria_rule__totally_ignore=True)
            .annotate(
                response_choice_name=F(f"response_choice_{locale}"),
                response_choice_id=F("id"),
                ignore_for_acceptability_threshold=F(
                    "representativity_criteria_rule__ignore_for_acceptability_threshold"
                ),
            )
            .values(
                "response_choice_id",
                "response_choice_name",
                "ignore_for_acceptability_threshold",
                "sort_order",
            )
            .annotate(
                total=Count(
                    "unique_choice_participationresponses",
                    filter=Q(
                        unique_choice_participationresponses__participation__assessment_id=self.assessment_id,
                        unique_choice_participationresponses__participation__user__is_unknown_user=False,
                    ),
                )
            )
            .order_by("sort_order")
        )

    @property
    def total_responses(self):
        return (
            self.representativity_criteria.profiling_question.participationresponses.filter(
                participation__assessment_id=self.assessment_id,
                participation__user__is_unknown_user=False,
            )
            .exclude(unique_choice_response=None)
            .count()
        )

    @property
    def acceptability_threshold_considered(self):
        if self.acceptability_threshold and (
            self.acceptability_threshold > self.representativity_criteria.min_rate
        ):
            return self.acceptability_threshold
        else:
            return self.representativity_criteria.min_rate

    @property
    def respected(self):
        total_response = self.total_responses
        if total_response == 0:
            return False
        return all(
            [
                (
                    (
                        (response_choice_count["total"] / total_response) * 100
                        >= self.acceptability_threshold_considered
                    )
                    if not response_choice_count["ignore_for_acceptability_threshold"]
                    else True
                )
                for response_choice_count in self.count_by_response_choice
            ]
        )
