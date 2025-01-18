from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.documents.models import Document
from django.utils.translation import gettext_lazy as _


@register_setting
class StructureSettings(BaseSiteSetting):
    email = models.EmailField(verbose_name=_("Adresse mail de contact"), blank=True)

    class Meta:
        verbose_name = _("Paramètre de la structure")


@register_setting
class RGPDSettings(BaseSiteSetting):
    legal_mention = models.ForeignKey(
        Document,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Mentions légales"),
    )
    terms_of_use = models.ForeignKey(
        Document,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Conditions générales d'utilisation"),
    )
    terms_of_sale = models.ForeignKey(
        Document,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Conditions générales de vente"),
    )
    confidentiality_policy = models.ForeignKey(
        Document,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Politique de confidentialité"),
    )
    content_license = models.ForeignKey(
        Document,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Licence Contenu"),
    )

    panels = [
        FieldPanel("legal_mention"),
        FieldPanel("terms_of_use"),
        FieldPanel("terms_of_sale"),
        FieldPanel("confidentiality_policy"),
        FieldPanel("content_license"),
    ]

    translated_fields = [
        "legal_mention",
        "terms_of_use",
        "terms_of_sale",
        "confidentiality_policy",
        "content_license",
    ]

    class Meta:
        verbose_name = "RGPD"


@register_setting
class ImportantPagesSettings(BaseSiteSetting):
    class Meta:
        verbose_name = _("Pages importantes")

    faq_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("FAQ"),
    )

    panels = [
        FieldPanel("faq_page"),
    ]
