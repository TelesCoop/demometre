from django import forms
from django.db import models
from django.db.models import Q
from django.utils import timezone
from model_utils.models import TimeStampedModel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import InlinePanel, FieldPanel
from wagtail.documents.models import Document
from wagtail.models import Orderable
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from my_auth.models import User
from open_democracy_back.constants import ASSESSMENT_DOCUMENT_CATEGORIES_CHOICES
from open_democracy_back.models.participation_models import Response
from open_democracy_back.models.utils import FrontendRichText
from open_democracy_back.utils import (
    InitiatorType,
    LocalityType,
    ManagedAssessmentType,
)


@register_snippet
class Region(index.Indexed, models.Model):
    code = models.CharField(max_length=3, verbose_name=_("Code"))
    name = models.CharField(max_length=64, verbose_name=_("Nom"))

    locality_type = LocalityType.REGION

    search_fields = [
        index.SearchField(
            "name",
        ),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Région")
        verbose_name_plural = _("Régions")


@register_snippet
class Department(index.Indexed, models.Model):
    code = models.CharField(max_length=3, verbose_name=_("Code"))
    name = models.CharField(max_length=64, verbose_name=_("Nom"))
    region = models.ForeignKey(
        Region,
        verbose_name=_("Région"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="departments",
    )

    locality_type = LocalityType.DEPARTMENT

    search_fields = [
        index.SearchField(
            "name",
        ),
    ]

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = _("Département")
        verbose_name_plural = _("Départements")


@register_snippet
class Municipality(index.Indexed, ClusterableModel):
    code = models.CharField(
        max_length=100,
        verbose_name=pgettext_lazy("unique code for a city", "Code insee"),
    )
    name = models.CharField(max_length=255, verbose_name=_("Nom"))
    department = models.ForeignKey(
        Department,
        verbose_name=_("Département"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="municipalities",
    )
    population = models.IntegerField(
        verbose_name=pgettext_lazy("number of inhabitants", "Population"), default=0
    )

    locality_type = LocalityType.MUNICIPALITY

    panels = [
        FieldPanel("code"),
        FieldPanel("name"),
        FieldPanel("department"),
        FieldPanel("population"),
        InlinePanel(
            "zip_codes",
            label=_("Code postal"),
        ),
    ]

    search_fields = [
        index.SearchField(
            "name",
        ),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Commune")
        verbose_name_plural = _("Communes")


class ZipCode(models.Model):
    code = models.CharField(max_length=100, verbose_name=_("Code"))
    municipality = ParentalKey(
        Municipality,
        verbose_name=_("Municipalité"),
        on_delete=models.CASCADE,
        related_name="zip_codes",
    )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _("Code postal")
        verbose_name_plural = _("Code postaux")


@register_snippet
class EPCI(index.Indexed, ClusterableModel):
    code = models.CharField(max_length=100, verbose_name=_("Code siren"))
    name = models.CharField(max_length=255, verbose_name=_("Nom"))
    population = models.IntegerField(verbose_name=_("Population"), default=0)

    locality_type = LocalityType.INTERCOMMUNALITY

    panels = [
        FieldPanel("code"),
        FieldPanel("name"),
        FieldPanel("population"),
        InlinePanel("related_municipalities_ordered", label=_("Liste des communes")),
    ]

    search_fields = [
        index.SearchField(
            "name",
        ),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Intercommunalité")
        verbose_name_plural = _("Intercommunalités")


class MunicipalityOrderByEPCI(Orderable):
    epci = ParentalKey(
        EPCI, on_delete=models.CASCADE, related_name="related_municipalities_ordered"
    )
    municipality = models.ForeignKey(
        Municipality, on_delete=models.CASCADE, verbose_name=_("Commune")
    )
    panels = [
        FieldPanel("municipality"),
    ]


@register_snippet
class AssessmentType(models.Model):
    assessment_type = models.CharField(
        max_length=32,
        choices=ManagedAssessmentType.choices,
        verbose_name=_("type d'évaluation"),
        unique=True,
        editable=False,
    )
    publish_results_regardless_of_representativities = models.BooleanField(
        verbose_name="publier les résultats sans tenir compte des critères de représentativité",
        default=False,
    )
    for_who = models.CharField(
        max_length=510, blank=True, verbose_name=_("A qui c'est adressé")
    )
    what = models.CharField(
        max_length=510, blank=True, verbose_name=_("Ce que ça contient")
    )
    for_what = models.CharField(
        max_length=510, blank=True, verbose_name=_("Ce que ça permet")
    )
    results = models.CharField(
        max_length=510, blank=True, verbose_name=_("Les résultats")
    )
    price = models.CharField(max_length=510, blank=True, verbose_name=_("Le prix"))
    pdf = models.ForeignKey(
        Document,
        verbose_name=_("Pdf du questionnaire"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("publish_results_regardless_of_representativities"),
        FieldPanel("for_who", widget=forms.Textarea),
        FieldPanel("what", widget=forms.Textarea),
        FieldPanel("for_what", widget=forms.Textarea),
        FieldPanel("results", widget=forms.Textarea),
        FieldPanel("price", widget=forms.Textarea),
        FieldPanel("pdf"),
    ]

    translated_fields = [
        "for_who",
        "what",
        "for_what",
        "results",
        "price",
    ]

    def __str__(self):
        return self.get_assessment_type_display()

    class Meta:
        verbose_name = _("Type d'évaluation")
        verbose_name_plural = _("Types d'évaluation")


class AssessmentQueryset(models.QuerySet):
    def filter_has_details(self, user_id):
        return self.filter(
            Q(initiated_by_user_id=user_id) | Q(experts__id=user_id)
        ).distinct()


@register_snippet
class Assessment(TimeStampedModel, ClusterableModel):
    assessment_type = models.ForeignKey(
        AssessmentType,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Type d'évaluation"),
    )
    survey = models.ForeignKey(
        "Survey",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Questionnaire"),
    )
    conditions_of_sale_consent = models.BooleanField(default=False)
    end_date = models.DateField(null=True, blank=True, verbose_name=_("Date de fin"))

    experts = models.ManyToManyField(
        User,
        blank=True,
        verbose_name=_("Experts"),
        related_name="assessments",
        limit_choices_to={"groups__name": "Experts"},
        help_text=_(
            "Pour ajouter un expert à la liste il faut créer / modifier l'utilisateur correspondant, aller dans l'onglet rôles et cocher la case Experts"
        ),
    )
    initiated_by_user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Initialisé par"),
        related_name="initiated_assessments",
        help_text=_(
            "Si l'évaluation est initié au nom de la localité, quelqu'un peut tout de même être à la source"
        ),
    )
    initiator_type = models.CharField(
        "type d'initilisateur",
        max_length=32,
        choices=InitiatorType.choices,
        blank=True,
        null=True,
    )
    initiator_usage_consent = models.BooleanField(default=False)
    initialized_to_the_name_of = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Initialisé au nom de"),
    )
    initialization_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date d'initialisation"),
        help_text=_(
            "Si il n'y a pas de date d'initialisation, c'est que le début de l'évaluation n'a pas été confirmée"
        ),
    )
    is_initialization_questions_completed = models.BooleanField(default=False)
    last_participation_date = models.DateTimeField(
        default=timezone.now, verbose_name=_("Date de dernière participation")
    )
    locality_type = models.CharField(
        max_length=32,
        choices=LocalityType.choices,
        default=LocalityType.MUNICIPALITY,
        verbose_name=_("Type de localité"),
    )
    epci = models.ForeignKey(
        EPCI,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Intercommunalité"),
    )
    municipality = models.ForeignKey(
        Municipality,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Commune"),
    )
    region = models.ForeignKey(
        Region,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Région"),
    )
    department = models.ForeignKey(
        Department,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Département"),
    )
    name = models.CharField(verbose_name=_("nom"), max_length=80, blank=True, null=True)

    # details
    context = FrontendRichText(verbose_name=_("contexte"), blank=True, default="")
    objectives = FrontendRichText(verbose_name=_("objectifs"), blank=True, default="")
    stakeholders = FrontendRichText(
        verbose_name=_("parties prenantes"), blank=True, default=""
    )
    calendar = FrontendRichText(verbose_name=_("calendrier"), blank=True, default="")

    objects = AssessmentQueryset.as_manager()

    @property
    def published_results(self):
        if (
            self.assessment_type
            and self.assessment_type.publish_results_regardless_of_representativities
        ):
            return True
        return all(
            [
                representativity.respected
                for representativity in self.representativities.all()
            ]
        )

    @property
    def population(self):
        if self.locality_type == LocalityType.MUNICIPALITY:
            return self.municipality.population
        if self.locality_type == LocalityType.INTERCOMMUNALITY:
            return self.epci.population

    @property
    def collectivity_name(self):
        if self.locality_type == LocalityType.MUNICIPALITY:
            return self.municipality.name
        if self.locality_type == LocalityType.INTERCOMMUNALITY:
            return self.epci.name

    @property
    def code(self):
        if self.locality_type == LocalityType.MUNICIPALITY:
            return self.municipality.code
        if self.locality_type == LocalityType.INTERCOMMUNALITY:
            return self.epci.code

    panels = [
        FieldPanel("name"),
        FieldPanel("assessment_type"),
        FieldPanel("experts"),
        FieldPanel("locality_type"),
        FieldPanel("municipality"),
        FieldPanel("epci"),
        FieldPanel("initiated_by_user"),
        FieldPanel("initiator_type"),
        FieldPanel("initialized_to_the_name_of"),
        FieldPanel("initialization_date"),
        FieldPanel("end_date"),
        FieldPanel("context"),
        FieldPanel("objectives"),
        FieldPanel("stakeholders"),
        FieldPanel("calendar"),
        InlinePanel("documents", label="documents"),
        InlinePanel("payment", label="paiement"),
    ]

    def __str__(self):
        locality = None
        if self.locality_type == LocalityType.MUNICIPALITY:
            locality = self.municipality
        elif self.locality_type == LocalityType.INTERCOMMUNALITY:
            locality = self.epci
        elif self.locality_type == LocalityType.DEPARTMENT:
            locality = self.department
        elif self.locality_type == LocalityType.REGION:
            locality = self.region
        return f"{self.get_locality_type_display()} {locality}"

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.collectivity_name
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Évaluation")
        verbose_name_plural = _("Évaluations")


class AssessmentResponseQuerySet(models.QuerySet):
    def accounted_in_assessment(self, assessment_pk):
        # filter responses to include only those from target assessment and ignore those from anonymous users and passed responses
        return self.filter(
            answered_by__is_unknown_user=False,
            assessment_id=assessment_pk,
        ).exclude(has_passed=True)


# All questionnaire objective responses are assessment responses
class AssessmentResponse(Response):
    assessment = models.ForeignKey(
        Assessment, on_delete=models.CASCADE, related_name="responses"
    )
    answered_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="assessment_responses", null=True
    )

    objects = AssessmentResponseQuerySet.as_manager()

    class Meta:
        unique_together = ["assessment", "question"]


class AssessmentDocument(TimeStampedModel):
    assessment = ParentalKey(
        Assessment, on_delete=models.CASCADE, related_name=_("documents")
    )
    category = models.CharField(
        verbose_name=_("catégorie"),
        max_length=20,
        choices=ASSESSMENT_DOCUMENT_CATEGORIES_CHOICES,
    )
    file = models.FileField(verbose_name=_("fichier"))
    name = models.CharField(verbose_name=_("nom"), max_length=80)

    panels = [
        FieldPanel("category"),
        FieldPanel("file"),
        FieldPanel("name"),
    ]


class AssessmentPayment(TimeStampedModel):
    assessment = ParentalKey(
        Assessment, on_delete=models.CASCADE, unique=True, related_name="payment"
    )
    author = models.ForeignKey(
        User,
        verbose_name=_("auteur du paiement"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    amount = models.FloatField(verbose_name=_("montant"))

    panels = [
        FieldPanel("amount"),
        FieldPanel("author"),
    ]

    def __str__(self):
        return (
            f"assessment id {self.assessment.pk}, amount {self.amount},"
            f"by {self.author.email}"
        )
