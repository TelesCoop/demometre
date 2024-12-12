from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.utils import translation
from model_utils.models import TimeStampedModel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from taggit.models import TagBase
from wagtail import blocks
from wagtail.admin.panels import (
    InlinePanel,
    FieldRowPanel,
    MultiFieldPanel,
    HelpPanel,
    FieldPanel,
)
from wagtail.fields import RichTextField, StreamField
from wagtail.models import TranslatableMixin, Orderable
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from django.utils.translation import gettext_lazy as _

from open_democracy_back.utils import (
    NUMERICAL_OPERATOR,
    SIMPLE_RICH_TEXT_FIELD_FEATURE,
    BooleanOperator,
    QuestionType,
    PillarName,
    SurveyLocality,
)


@register_snippet
class Role(TranslatableMixin, ClusterableModel):
    name = models.CharField(verbose_name=_("Nom"), max_length=125)

    description = models.TextField(
        default="",
        null=True,
        blank=True,
        verbose_name=_("Description du rôle"),
        help_text=_("Texte précisant le rôle (définition, exemple, reformulation)."),
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        InlinePanel("related_markers_ordered", label=_("Ordre des marqueurs")),
    ]

    translated_fields = ["name", "description"]

    def __str__(self):
        locale = translation.get_language()
        return getattr(self, f"name_{locale}")

    def __init__(self, *args, **kwargs):
        """Fixes a bug when trying to translate."""
        if "index_entries" in kwargs:
            kwargs.pop("index_entries")
        super().__init__(*args, **kwargs)

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = _("Rôles")
        verbose_name = _("Rôle")


@register_snippet
class ProfileType(models.Model):
    name = models.CharField(max_length=125, default="")

    rules_intersection_operator = models.CharField(
        max_length=8, choices=BooleanOperator.choices, default=BooleanOperator.AND
    )

    panels = [
        FieldPanel("name"),
    ]

    translated_fields = ["name"]

    def name_with_rules_count(self):
        count = self.rules.count()
        return f"{str(self)} ({count} règle{'s' if count > 1 else ''})"

    def __str__(self):
        locale = translation.get_language()
        return getattr(self, f"name_{locale}") or self.name_fr

    class Meta:
        verbose_name_plural = _("Types de profil")
        verbose_name = _("Type de profil")


class ScoreFields(models.Model):
    score_1 = models.TextField(
        blank=True,
        verbose_name=_("Score = 1 (Signification)"),
        help_text=_("Signification du résultat 1, affiché dans le DémoMètre"),
        default="",
    )
    score_2 = models.TextField(
        blank=True,
        verbose_name=_("Score = 2 (Signification)"),
        help_text=_("Signification du résultat 2, affiché dans le DémoMètre"),
        default="",
    )
    score_3 = models.TextField(
        blank=True,
        verbose_name=_("Score = 3 (Signification)"),
        help_text=_("Signification du résultat 3, affiché dans le DémoMètre"),
        default="",
    )
    score_4 = models.TextField(
        blank=True,
        verbose_name=_("Score = 4 (Signification)"),
        help_text=_("Signification du résultat 4, affiché dans le DémoMètre"),
        default="",
    )

    panels = [FieldPanel(f"score_{i}") for i in range(1, 5)]
    panel_names = [f"score_{i}" for i in range(1, 5)]

    class Meta:
        abstract = True


@register_snippet
class Survey(TimeStampedModel):
    name = models.CharField(max_length=255, verbose_name=_("Nom"), unique=True)
    survey_locality = models.CharField(
        max_length=32,
        choices=SurveyLocality.choices,
        default=SurveyLocality.CITY,
        verbose_name=_("Échelon du questionnaire"),
        unique=True,
    )
    description = RichTextField(
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Description"),
        help_text=_("Description du questionnaire"),
        max_length=1024,
        default="",
    )
    code = models.CharField(
        max_length=10,
        verbose_name=_("code"),
        help_text=_("Nom court du questionnaire pour les menus de l'interface admin"),
        default="",
    )
    panels = [
        FieldPanel("name"),
        FieldPanel("survey_locality"),
        FieldPanel("code"),
        FieldPanel("description"),
    ]

    translated_fields = ["name", "description"]

    def __str__(self):
        return f"{self.name} ({self.code})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        [child_pillar.save() for child_pillar in self.pillars.all()]

    class Meta:
        verbose_name_plural = _("Questionnaires")
        verbose_name = _("Questionnaire")


@register_snippet
class Pillar(models.Model):
    name = models.CharField(
        verbose_name=_("Nom"), max_length=125, choices=PillarName.choices
    )
    code = models.CharField(
        verbose_name=_("Code"),
        max_length=10,
        help_text=_("Correspond au numéro (ou lettre) de ce pilier"),
    )
    order = models.IntegerField(
        verbose_name=_("Ordre"),
        help_text=_("Permet de ranger dans l'ordre voulu les piliers"),
        default="1",
    )

    description = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Description"),
        help_text=_("Description pour le référentiel"),
    )

    survey = models.ForeignKey(
        Survey,
        null=True,
        on_delete=models.CASCADE,
        related_name="pillars",
    )

    panels = [
        FieldPanel("code"),
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("survey"),
    ]

    translated_fields = ["description"]

    def __str__(self):
        return f"{self.survey.code}.{self.code}: {self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        [child_marker.save() for child_marker in self.markers.all()]

    class Meta:
        verbose_name_plural = _("1. Piliers")
        verbose_name = _("1. Pilier")
        ordering = ["order"]


@register_snippet
class Marker(index.Indexed, ScoreFields):
    pillar = models.ForeignKey(
        Pillar, null=True, blank=True, on_delete=models.CASCADE, related_name="markers"
    )
    name = models.CharField(verbose_name=_("Nom"), max_length=125)
    code = models.CharField(
        verbose_name=_("Code"),
        max_length=3,
        help_text=_("Correspond au numéro (ou lettre) de ce marqueur dans son pilier"),
    )
    concatenated_code = models.CharField(max_length=10, default="")
    description = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Description"),
        help_text=_("Description pour le référentiel"),
    )

    panels = [
        FieldPanel("pillar"),
        FieldPanel("name"),
        FieldPanel("code"),
        FieldPanel("description"),
    ] + ScoreFields.panels

    translated_fields = ["name", "description"] + ScoreFields.panel_names

    search_fields = [
        index.SearchField(
            "name",
        ),
    ]

    def __str__(self):
        return f"{self.concatenated_code}: {self.name}"

    def save(self, *args, **kwargs):
        code_elements = []
        if self.pillar:
            if self.pillar.survey:
                code_elements.append(self.pillar.survey.code)
            code_elements.append(self.pillar.code)
        code_elements.append(self.code)
        self.concatenated_code = ".".join(code_elements)
        super().save(*args, **kwargs)
        [child_criteria.save() for child_criteria in self.criterias.all()]

    class Meta:
        verbose_name_plural = _("2. Marqueurs")
        verbose_name = _("2. Marqueur")
        ordering = ["code"]


class MarkerOrderByRole(Orderable):
    role = ParentalKey(
        Role, on_delete=models.CASCADE, related_name="related_markers_ordered"
    )
    marker = models.ForeignKey(Marker, on_delete=models.CASCADE)
    panels = [
        FieldPanel("marker"),
    ]


@register_snippet
class ThematicTag(TagBase):
    class Meta:
        verbose_name = _("Thématique")
        verbose_name_plural = _("Thématiques")


explanatory_args = [
    (
        "category",
        blocks.StructBlock(
            [
                ("title", blocks.CharBlock(label=_("Titre"))),
                (
                    "description",
                    blocks.RichTextBlock(
                        label=_("Description"),
                        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
                    ),
                ),
            ],
            label_format=_("Catégorie : {title}"),
            label=_("Catégorie"),
        ),
    )
]
explanatory_kwargs = {
    "blank": True,
    "verbose_name": _(
        "Explicatif du critère (sources, exemples, obligations légales ...)"
    ),
    "use_json_field": True,
}


@register_snippet
class Criteria(index.Indexed, ClusterableModel):
    marker = models.ForeignKey(
        Marker,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="criterias",
    )
    name = models.CharField(verbose_name=_("Nom"), max_length=125)
    code = models.IntegerField(
        verbose_name=_("Code"),
        help_text=_("Correspond au numéro de ce critère dans son marqueur"),
        validators=[MaxValueValidator(100), MinValueValidator(1)],
    )
    concatenated_code = models.CharField(max_length=12, default="")
    thematic_tags = models.ManyToManyField(
        ThematicTag, blank=True, verbose_name=_("Thématiques")
    )
    description = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Description"),
        help_text=_("Description pour le référentiel"),
    )

    explanatory = StreamField(
        explanatory_args,
        **explanatory_kwargs,
    )
    explanatory_fr = StreamField(
        explanatory_args,
        **{
            **explanatory_kwargs,
            "verbose_name": _(
                "Explicatif du critère (sources, exemples, obligations légales ...) (fr)"
            ),
            "null": True,
        },
    )
    explanatory_en = StreamField(
        explanatory_args,
        **{
            **explanatory_kwargs,
            "verbose_name": _(
                "Explicatif du critère (sources, exemples, obligations légales ...) (en)"
            ),
            "null": True,
        },
    )

    panels = [
        FieldPanel("marker"),
        FieldPanel("name"),
        FieldPanel("code"),
        FieldPanel("thematic_tags", widget=forms.CheckboxSelectMultiple),
        FieldPanel("description"),
        InlinePanel("related_definition_ordered", label=_("Définitions")),
        FieldPanel("explanatory"),
    ]

    translated_fields = ["name", "description", "explanatory"]

    search_fields = [
        index.SearchField(
            "name",
        )
    ]

    def __str__(self):
        locale = translation.get_language()
        return f"{self.concatenated_code}: {getattr(self, f'name_{locale}')}"

    def save(self, *args, **kwargs):
        code_elements = []
        if self.marker:
            code_elements.append(self.marker.concatenated_code)
        code_elements.append(str(self.code))
        self.concatenated_code = ".".join(code_elements)
        super().save(*args, **kwargs)
        # Use proxy QuestionnaireQuestion
        child_questions = QuestionnaireQuestion.objects.filter(criteria_id=self.id)
        [child_question.save() for child_question in child_questions]

    class Meta:
        verbose_name_plural = _("3. Critères")
        verbose_name = _("3. Critère")
        ordering = ["code"]


@register_snippet
class Definition(models.Model):
    word = models.CharField(max_length=255, verbose_name=_("mot"))
    explanation = RichTextField(
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE, verbose_name=_("explication")
    )

    translated_fields = ["word", "explanation"]

    def __str__(self):
        return f"Définition de {self.word}"

    class Meta:
        verbose_name = _("Définition")
        verbose_name_plural = _("Définitions")


class CriteriaDefinition(Orderable):
    criteria = ParentalKey(
        Criteria, on_delete=models.CASCADE, related_name="related_definition_ordered"
    )
    definition = models.ForeignKey(Definition, on_delete=models.CASCADE)
    panels = [
        FieldPanel("definition"),
    ]


class QuestionQuerySet(models.QuerySet):
    def filter_by_population(self, population):
        return self.filter(
            Q(population_lower_bound__lte=population) | Q(population_lower_bound=None),
            Q(population_upper_bound__gte=population) | Q(population_upper_bound=None),
        )

    def filter_by_role(self, role):
        return self.filter(Q(roles=role) | Q(roles__isnull=True))

    def filter_by_profiles(self, profiles):
        return self.filter(Q(profiles__in=profiles) | Q(profiles__isnull=True))


class QuestionManager(models.Manager):
    def get_queryset(self):
        return QuestionQuerySet(self.model, using=self._db)

    def filter_by_population(self, population):
        return self.get_queryset().filter_by_population(population)

    def filter_by_role(self, role):
        return self.get_queryset().filter_by_role(role)

    def filter_by_profiles(self, profiles):
        return self.get_queryset().filter_by_profiles(profiles)


@register_snippet
class Question(index.Indexed, TimeStampedModel, ClusterableModel):
    objects = QuestionManager()

    rules_intersection_operator = models.CharField(
        max_length=8, choices=BooleanOperator.choices, default=BooleanOperator.AND
    )

    code = models.CharField(
        verbose_name=_("Code"),
        max_length=2,
        help_text=_(
            "Correspond au numéro (ou lettre) de cette question, détermine son ordre"
        ),
    )
    concatenated_code = models.CharField(max_length=11, default="")

    name = models.CharField(verbose_name=_("Nom"), max_length=125, default="")
    question_statement = models.TextField(
        verbose_name=_("Enoncé de la question"), default=""
    )

    mandatory = models.BooleanField(default=False, verbose_name=_("Obligatoire"))

    type = models.CharField(
        max_length=32,
        choices=QuestionType.choices,
        default=QuestionType.BOOLEAN,
        help_text=_("Choisir le type de question"),
    )

    population_lower_bound = models.IntegerField(
        verbose_name=_("Borne inférieure (population min)"),
        blank=True,
        null=True,
        help_text=_(
            "Si aucune valeur n'est renseignée, aucune borne inférieur ne sera prise en compte"
        ),
    )
    population_upper_bound = models.IntegerField(
        verbose_name=_("Borne suppérieur (population max)"),
        blank=True,
        null=True,
        help_text=_(
            "Si aucune valeur n'est renseignée, aucune borne suppérieur ne sera prise en compte"
        ),
    )

    allows_to_explain = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="explained_by",
        verbose_name=_("Permet d'expliciter une autre question"),
    )

    max_multiple_choices = models.IntegerField(
        verbose_name=_("Nombre maximal de choix possible"),
        blank=True,
        null=True,
        help_text=_(
            "Pour une question à choix multiple, indiquer le nombre maximum de choix possible"
        ),
    )

    min_number_value = models.FloatField(
        verbose_name=_("Valeur minimale du champ nombre"), blank=True, null=True
    )
    max_number_value = models.FloatField(
        verbose_name=_("Valeur maximale du champ nombre"), blank=True, null=True
    )
    step_number_value = models.FloatField(
        verbose_name=_("Granularité minimale du champ nombre (ex: 1, 0.1, 0.01, ...)"),
        blank=True,
        null=True,
    )

    description = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Description"),
        help_text=_("Texte précisant la question et pourquoi elle est posée."),
    )

    comments = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name=_("Commentaires (pour l'interne)"),
        help_text=_("Indication affichée uniquement pour les administrateurs."),
    )

    # Questionnary questions fields
    criteria = models.ForeignKey(
        Criteria,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    objectivity = models.CharField(
        max_length=32,
        choices=[("objective", _("Objective")), ("subjective", _("Subjective"))],
        default="subjective",
        verbose_name=_("Objective / Subjective (Non modifiable)"),
        help_text=_("Ce champ n'est pas modifiable après la création de la question"),
    )
    method = models.CharField(
        max_length=32,
        choices=[
            ("quantitative", _("Quantitative")),
            ("qualitative", _("Qualitative")),
        ],
        blank=True,
        verbose_name=_("Methode"),
    )
    profiles = models.ManyToManyField(
        ProfileType,
        verbose_name=_("Profils concernés"),
        related_name="questions_that_depend_on_me",
        blank=True,
    )
    assessment_types = models.ManyToManyField(
        "open_democracy_back.AssessmentType",
        verbose_name=_("Types d'évaluation concernés"),
        related_name="questions",
        blank=True,
    )

    # Profiling questions fields
    profiling_question = models.BooleanField(default=False)
    # this is only for profiling questions
    surveys = models.ManyToManyField(
        Survey,
        verbose_name=_("Questionnaires concernés"),
        related_name="profiling_questions",
        blank=True,
    )

    roles = models.ManyToManyField(
        Role,
        blank=True,
        verbose_name=_("Rôles concernés"),
        help_text=_("Si aucun rôle n'est sélectionné c'est comme si tous l'étaient"),
    )

    @property
    def survey_type(self):
        return "profiling" if self.profiling_question else "questionnaire"

    search_fields = [
        index.SearchField(
            "question_statement",
        ),
        index.SearchField(
            "name",
        ),
    ]

    principal_panels = [
        FieldPanel("code"),
        FieldPanel("name"),
        FieldPanel("question_statement"),
        FieldPanel("description"),
        FieldPanel("mandatory"),
        FieldRowPanel(
            [
                FieldPanel("population_lower_bound"),
                FieldPanel("population_upper_bound"),
            ],
            heading=_("Taille des collectivités concernées"),
        ),
        FieldPanel("roles", widget=forms.CheckboxSelectMultiple),
    ]

    commun_types_panels = [
        FieldPanel("type"),
        InlinePanel(
            "response_choices",
            label=_("Choix de réponses possibles"),
        ),
        FieldPanel("max_multiple_choices"),
        InlinePanel(
            "categories",
            label=_("Catégories pour une question fermée à échelle"),
        ),
    ]

    explanation_panels = [
        FieldPanel("allows_to_explain"),
        FieldPanel("comments"),
    ]

    translated_fields = ["name", "question_statement", "description", "comments"]

    RESPONSE_NAME_BY_QUESTION_TYPE = {
        QuestionType.PERCENTAGE.value: "percentage_response",
        QuestionType.NUMBER.value: "number_response",
        QuestionType.BOOLEAN.value: "boolean_response",
        QuestionType.UNIQUE_CHOICE.value: "unique_choice_response",
        QuestionType.MULTIPLE_CHOICE.value: "multiple_choice_response",
    }

    RESPONSE_RANGES_BY_QUESTION_TYPE = {
        QuestionType.PERCENTAGE.value: "percentage_ranges",
        QuestionType.NUMBER.value: "number_ranges",
    }

    def __str__(self):
        if self.profiling_question:
            return f"{_('Profilage')}: {self.name_fr}"
        return f"{self.concatenated_code}: {self.name_fr}"

    def clean(self):
        if self.type == QuestionType.NUMBER.value:
            if self.step_number_value is None:
                raise ValidationError(
                    _("La granularité du champ nombre doit être renseignée"),
                    code="invalid",
                )

    def save(self, *args, **kwargs):
        # Passing from objectivity to subjectivity is not allowed
        if self.id:
            old_value = Question.objects.get(id=self.id)
            self.objectivity = old_value.objectivity
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["code"]


class QuestionnaireQuestionManager(QuestionManager):
    def get_queryset(self):
        return super().get_queryset().filter(profiling_question=False)


def get_number_multifield_panel(is_profiling_question=False):
    panels = [
        FieldPanel("min_number_value"),
        FieldPanel("max_number_value"),
        FieldPanel("step_number_value"),
    ]
    if not is_profiling_question:
        panels.append(
            HelpPanel(
                '<div class="help-block help-info">'
                + _(
                    "Attention à prendre en compte la granularité dans les bornes des scores associés"
                )
                + '</div">'
            )
        )
        panels.append(
            InlinePanel(
                "number_ranges",
                label=_("Score associé aux réponses d'une question nombre"),
            )
        )

    return MultiFieldPanel(
        panels,
        heading=_("Paramétrage d'une question de nombre"),
        classname="collapsible number-question-panel",
    )


@register_snippet
class QuestionnaireQuestion(Question):
    objects = QuestionnaireQuestionManager()

    panels = [
        FieldPanel("criteria"),
        *Question.principal_panels,
        FieldPanel("profiles", widget=forms.CheckboxSelectMultiple),
        FieldPanel("assessment_types", widget=forms.CheckboxSelectMultiple),
        FieldPanel("objectivity"),
        FieldPanel("method"),
        *Question.commun_types_panels,
        InlinePanel(
            "percentage_ranges",
            label=_("Score associé aux réponses d'une question de pourcentage"),
        ),
        get_number_multifield_panel(),
        *Question.explanation_panels,
    ]

    search_fields = [
        *Question.search_fields,
        index.FilterField("profiling_question"),
    ]

    def save(self, *args, **kwargs):
        self.profiling_question = False
        self.concatenated_code = (
            self.criteria.concatenated_code + "." if self.criteria else ""
        ) + self.code

        super().save(*args, **kwargs)

    class Meta(Question.Meta):
        verbose_name_plural = _("4. Questions")
        verbose_name = _("4. Question")
        proxy = True


class ProfilingQuestionManager(QuestionManager):
    def get_queryset(self):
        return super().get_queryset().filter(profiling_question=True)


@register_snippet
class ProfilingQuestion(Question):
    objects = ProfilingQuestionManager()

    panels = [
        *Question.principal_panels,
        *Question.commun_types_panels,
        FieldPanel("surveys", widget=forms.CheckboxSelectMultiple),
        *Question.explanation_panels,
        get_number_multifield_panel(True),
    ]

    # TODO : the search not works because filter on profiling_question=True
    search_fields = [
        *Question.search_fields,
        index.FilterField("profiling_question"),
    ]

    def save(self, *args, **kwargs):
        self.profiling_question = True
        super().save(*args, **kwargs)

    class Meta(Question.Meta):
        verbose_name_plural = _("Questions de Profilage")
        verbose_name = _("Question de Profilage")
        proxy = True


SCORE_MAP = {
    4: 1,
    3: 2 / 3,
    2: 1 / 3,
    1: 0,
}


class Score(models.Model):
    associated_score = models.IntegerField(
        verbose_name=_("Score associé"),
        blank=True,
        null=True,
        help_text=_("Si pertinent"),
        validators=[MinValueValidator(1), MaxValueValidator(4)],
    )

    linearized_score = models.FloatField(
        verbose_name=_("Score associé linéarisé"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )

    @staticmethod
    def update_score(sender, **kwargs):
        instance = kwargs.get("instance")
        if instance.associated_score is not None:
            instance.linearized_score = SCORE_MAP[instance.associated_score]
        else:
            instance.linearized_score = None

    class Meta:
        abstract = True


class ResponseChoice(TimeStampedModel, Orderable, Score):
    question = ParentalKey(
        Question, on_delete=models.CASCADE, related_name="response_choices"
    )

    response_choice = models.CharField(
        max_length=510, default="", verbose_name=_("Réponse possible")
    )

    description = models.TextField(
        default="",
        null=True,
        blank=True,
        verbose_name=_("Description de la réponse"),
        help_text=_(
            "Texte précisant la réponse (définition, exemple, reformulation). Si la question est fermée à échelle la description ne s'affichera pas."
        ),
    )
    panels = [
        FieldPanel("response_choice"),
        FieldPanel("description"),
        FieldPanel("associated_score"),
    ]

    translated_fields = ["response_choice", "description"]

    def __str__(self):
        return self.response_choice_fr

    class Meta:
        verbose_name_plural = _("Choix de réponse")
        verbose_name = _("Choix de réponse")
        ordering = ["sort_order"]


# Update linearized score on save
pre_save.connect(Score.update_score, sender=ResponseChoice)


class PercentageRange(TimeStampedModel, Orderable, Score):
    question = ParentalKey(
        Question, on_delete=models.CASCADE, related_name="percentage_ranges"
    )

    lower_bound = models.IntegerField(
        verbose_name=_("Borne inférieure"),
        help_text=_("Si la réponse est suppérieur ou égale à"),
    )

    upper_bound = models.IntegerField(
        verbose_name=_("Borne suppérieure"),
        help_text=_("Si la réponse est inférieur ou égale à"),
    )

    panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [FieldPanel("lower_bound"), FieldPanel("upper_bound")],
                ),
                FieldPanel("associated_score"),
            ],
            heading=_("Score associé à une fourchette de pourcentage"),
        ),
    ]

    @property
    def str_boundaries(self):
        return f"{self.lower_bound}% à {self.upper_bound}%"

    def __str__(self):
        return f"{self.question} : {self.str_boundaries} = {self.associated_score}"

    def clean(self):
        if self.lower_bound > self.upper_bound:
            raise ValidationError(
                _(
                    "La borne inférieure doit être inférieure ou égale à la borne supérieure"
                )
            )

    class Meta:
        verbose_name_plural = _("Scores pour les différentes fourchettes")
        verbose_name = _("Score pour une fourchette donnée")
        ordering = ["sort_order"]


class NumberRange(TimeStampedModel, Orderable, Score):
    question = ParentalKey(
        Question, on_delete=models.CASCADE, related_name="number_ranges"
    )

    lower_bound = models.FloatField(
        verbose_name=_("Borne inférieure"),
        help_text=_("Si la réponse est suppérieur ou égale à"),
        null=True,
        blank=True,
    )

    upper_bound = models.FloatField(
        verbose_name=_("Borne suppérieure"),
        help_text=_("Si la réponse est inférieur ou égale à"),
        null=True,
        blank=True,
    )

    panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [FieldPanel("lower_bound"), FieldPanel("upper_bound")],
                ),
                FieldPanel("associated_score"),
            ],
            heading=_("Score associé à une fourchette de nombre"),
        ),
    ]

    @property
    def str_boundaries(self):
        if self.lower_bound is None:
            return f"=< {self.upper_bound}"
        elif self.upper_bound is None:
            return f">= {self.lower_bound}"
        else:
            return f">= {self.lower_bound} and <= {self.upper_bound}"

    def __str__(self):
        return f"{self.question}: {self.str_boundaries} = {self.associated_score}"

    def clean(self):
        if self.lower_bound is None and self.upper_bound is None:
            raise ValidationError(
                _("Au moins une borne doit être renseignée"),
                code="invalid",
            )
        if (
            self.lower_bound is not None
            and self.upper_bound is not None
            and self.lower_bound > self.upper_bound
        ):
            raise ValidationError(
                _(
                    "La borne inférieure doit être inférieure ou égale à la borne supérieure"
                )
            )

    class Meta:
        verbose_name_plural = _("Scores pour les différentes fourchettes")
        verbose_name = _("Score pour une fourchette donnée")
        ordering = ["sort_order"]


# Update linearized score on save
pre_save.connect(Score.update_score, sender=PercentageRange)
pre_save.connect(Score.update_score, sender=NumberRange)


class Category(TimeStampedModel, Orderable):
    question = ParentalKey(
        Question, on_delete=models.CASCADE, related_name="categories"
    )

    category = models.CharField(
        max_length=128,
        default="",
        verbose_name=_("Category"),
        help_text=_(
            "Permet de répondre à la même question pour différentes catégories"
        ),
    )

    translated_fields = ["category"]

    def __str__(self):
        locale = translation.get_language()
        return getattr(self, f"category_{locale}")

    class Meta:
        verbose_name = _("Category")
        ordering = ["sort_order"]


class GenericRule(TimeStampedModel, Orderable, ClusterableModel):
    """
    GenericRule define the response that must be done to a conditional question
    """

    class Meta:
        abstract = True

    conditional_question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name=_("Filter by question"),
        related_name="%(class)s_that_depend_on_me",
        null=True,
        blank=False,
    )

    # if conditional question is unique or multiple choices type
    response_choices = models.ManyToManyField(ResponseChoice)

    # if conditional question is percentage or number
    numerical_operator = models.CharField(
        max_length=8, choices=NUMERICAL_OPERATOR, blank=True, null=True
    )
    numerical_value = models.IntegerField(blank=True, null=True)
    float_value = models.FloatField(blank=True, null=True)

    # if conditional question is boolean
    boolean_response = models.BooleanField(blank=True, null=True)

    @property
    def type(self):
        return self.conditional_question.type

    @staticmethod
    def format_explanation(question_code, response):
        return _(
            "La réponse de la question d'affinage %(question_code)s doit être %(response)s"
        ) % {"question_code": question_code, "response": response}

    @staticmethod
    def explain_choice_rule(rule):
        response_choices = ", ".join(
            [
                response_choice.response_choice_fr
                for response_choice in rule.response_choices.all()
            ]
        )
        return rule.format_explanation(
            rule.conditional_question.code,
            _("égale à %(response_choices)s") % {"response_choices": response_choices},
        )

    RULE_EXPLANATION_BY_TYPE = {
        QuestionType.BOOLEAN.value: lambda rule: rule.format_explanation(
            rule.conditional_question.code,
            _("Oui") if rule.boolean_response else _("Non"),
        ),
        QuestionType.UNIQUE_CHOICE.value: explain_choice_rule,
        QuestionType.MULTIPLE_CHOICE.value: explain_choice_rule,
        QuestionType.NUMBER.value: lambda rule: rule.format_explanation(
            rule.conditional_question.code,
            f"{rule.numerical_operator} - {rule.numerical_value}",
        ),
        QuestionType.PERCENTAGE.value: lambda rule: rule.format_explanation(
            rule.conditional_question.code,
            f"{rule.numerical_operator} - {rule.numerical_value}%",
        ),
    }

    @property
    def explanation(self):
        return (
            self.RULE_EXPLANATION_BY_TYPE[self.conditional_question.type](self)
            if self.conditional_question.type in self.RULE_EXPLANATION_BY_TYPE
            else "Règle non prise en charge"
        )

    def __str__(self):
        condition_question_str = ""
        if self.conditional_question:
            if self.boolean_response:
                condition_question_str = "answer=" + str(self.boolean_response)
            elif self.numerical_operator:
                condition_question_str = (
                    f"answer{str(self.numerical_operator)}{str(self.numerical_value)}"
                )
            elif self.response_choices:
                for response_choice in self.response_choices.all():
                    condition_question_str += f"answer={str(response_choice)}, "

        return f"(ID: {str(self.id)}) {str(self.conditional_question)}, {condition_question_str}"

    RULE_FIELDS_TO_CLEAN = [
        "numerical_operator",
        "numerical_value",
        "float_value",
        "boolean_response",
    ]
    FIELDS_TO_NOT_CLEAN_BY_QUESTION_TYPE = {
        QuestionType.UNIQUE_CHOICE.value: [],  # type: ignore
        QuestionType.MULTIPLE_CHOICE.value: [],  # type: ignore
        QuestionType.PERCENTAGE.value: [  # type: ignore
            "numerical_operator",
            "numerical_value",
        ],
        QuestionType.NUMBER.value: [  # type: ignore
            "numerical_operator",
            "float_value",
        ],
        QuestionType.BOOLEAN.value: [  # type: ignore
            "boolean_response",
        ],
    }

    def save(self, *args, **kwargs):
        # Make sure the data is consistent with the question type
        if self.conditional_question.type in self.FIELDS_TO_NOT_CLEAN_BY_QUESTION_TYPE:
            fields_to_clean = [
                field
                for field in self.RULE_FIELDS_TO_CLEAN
                if field
                not in self.FIELDS_TO_NOT_CLEAN_BY_QUESTION_TYPE[
                    self.conditional_question.type
                ]
            ]
            for field_to_clean in fields_to_clean:
                setattr(self, field_to_clean, None)

        super().save(*args, **kwargs)


class QuestionRule(GenericRule):
    """
    Manage drawer questions :
    A QuestionRule can define if a profiling question must be show depending on another profiling question answer
    A QuestionRule can define if a questionnaire question must be show depending on another questionnaire question answer
    A QuestionRule can define if a questionnaire question must be show depending on profile type
    """

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="rules",
        null=True,
        blank=True,
    )


class ProfileDefinition(GenericRule):
    """
    Define profile type :
    A ProfileDefinition can define the definition of a profile type depending on profiling question answer
    """

    profile_type = models.ForeignKey(
        ProfileType,
        on_delete=models.CASCADE,
        related_name="rules",
        null=True,
        blank=True,
    )
