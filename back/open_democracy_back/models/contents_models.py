import datetime

from django import forms
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import translation
from django.utils.text import slugify
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import TranslatableMixin
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from django.utils.translation import gettext_lazy as _

from open_democracy_back.models.questionnaire_and_profiling_models import Pillar
from open_democracy_back.models.utils import BODY_FIELD_PARAMS


@register_snippet
class Feedback(index.Indexed, models.Model):
    picture = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Photo",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    person_name = models.CharField(max_length=64, verbose_name="Prénom et nom")
    person_context = models.CharField(
        max_length=64,
        verbose_name=_("Context de la personne"),
        help_text=_(
            "Exemple : Elu de Strasbourg, Membre de Démocratie Ouverte, Habitant de Toulouse ... "
        ),
    )
    quote = models.CharField(max_length=255, default="", verbose_name="Citation")
    publish = models.BooleanField(
        default=False, verbose_name=_("Publier dans la page d'accueil")
    )
    external_link = models.CharField(
        verbose_name=_("Lien externe"), blank=True, null=True, max_length=300
    )

    panels = [
        FieldPanel("person_name"),
        FieldPanel("picture"),
        FieldPanel("person_context"),
        FieldPanel("quote", widget=forms.Textarea),
        FieldPanel("external_link"),
        FieldPanel("publish"),
    ]

    translated_fields = [
        "person_context",
        "quote",
    ]

    search_fields = [
        index.SearchField(
            "person_name",
        ),
    ]

    def __str__(self):
        return self.person_name + (" (publié)" if self.publish else "")

    class Meta:
        verbose_name = _("Retour d'expériences")
        verbose_name_plural = _("Retours d'expériences")


class Article(index.Indexed, models.Model):
    image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Image principale",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    title = models.CharField(max_length=128, verbose_name=_("titre"))
    slug = models.CharField(max_length=150, blank=True, null=True)
    publication_date = models.DateTimeField(
        verbose_name=_("Date de publication"),
        default=datetime.datetime.now,
        help_text=_("Permet de trier l'ordre d'affichage des articles de blog"),
    )
    short_description = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
        verbose_name=_("Description courte"),
        help_text=_("Ce texte apparait sur la miniature"),
    )
    content = StreamField(
        BODY_FIELD_PARAMS,
        blank=True,
        verbose_name=_("Contenu"),
        help_text=_("Corps de l'article"),
        use_json_field=True,
    )
    external_link = models.URLField(
        verbose_name=_("Lien externe"),
        blank=True,
        null=True,
        max_length=300,
        help_text=_("Si ce champ est rempli, le corps de l'article sera ignoré"),
    )
    pillars = models.ManyToManyField(
        Pillar, related_name="%(class)ss", blank=True, verbose_name="Piliers concernés"
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("image"),
        FieldPanel("publication_date"),
        FieldPanel("short_description", widget=forms.Textarea),
        FieldPanel("content"),
        FieldPanel("external_link"),
        FieldPanel("pillars", widget=forms.CheckboxSelectMultiple),
    ]

    search_fields = [
        index.SearchField(
            "title",
        ),
    ]

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(**kwargs)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


@register_snippet
class BlogPost(TranslatableMixin, Article):
    class Meta(TranslatableMixin.Meta):
        verbose_name = _("Article de blog")
        verbose_name_plural = _("Articles de blog")
        ordering = ["-publication_date"]


@register_snippet
class Resource(TranslatableMixin, Article):
    class Meta(TranslatableMixin.Meta):
        verbose_name = _("Ressource")
        verbose_name_plural = _("Ressources")
        ordering = ["-publication_date"]


@register_snippet
class Partner(index.Indexed, models.Model):
    name = models.CharField(max_length=64, verbose_name=_("Nom"))
    logo_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Logo"),
        on_delete=models.CASCADE,
        related_name="+",
    )
    height = models.IntegerField(
        validators=[MinValueValidator(40), MaxValueValidator(120)],
        default=60,
        help_text=_("Choisir la hauteur du logo (min 40px / max 120px)"),
        verbose_name=_("Hauteur"),
    )
    show_in_home_page = models.BooleanField(
        default=True, verbose_name=_("Afficher dans la page d'accueil")
    )

    panels = [
        FieldPanel("name"),
        MultiFieldPanel(
            [
                FieldPanel("logo_image"),
                FieldPanel("height"),
            ],
            heading=_("Logo du partenaire"),
        ),
        FieldPanel("show_in_home_page"),
    ]

    search_fields = [
        index.SearchField(
            "name_fr",
        ),
        index.SearchField(
            "name_en",
        ),
    ]

    translated_fields = ["name"]

    def __str__(self):
        locale = translation.get_language()
        return getattr(self, f"name_{locale}")

    class Meta:
        verbose_name = _("Partenaire")
        verbose_name_plural = _("Partenaires")


@register_snippet
class Person(index.Indexed, models.Model):
    name = models.CharField(max_length=64, verbose_name=_("Nom"))
    image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Image"),
        on_delete=models.CASCADE,
        related_name="+",
    )
    job_title = models.CharField(
        max_length=136,
        verbose_name=_("Intitulé du poste"),
    )

    panels = [
        FieldPanel("image"),
        FieldPanel("name"),
        FieldPanel("job_title"),
    ]

    search_fields = [
        index.SearchField(
            "name",
        ),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Personne")
        verbose_name_plural = _("Personnes")
