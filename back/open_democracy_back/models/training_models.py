from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from wagtail.documents.models import Document


class Training(TimeStampedModel):
    class Meta:
        verbose_name = _("Formation")

    name = models.CharField(verbose_name=_("nom"), max_length=100)
    audience = models.CharField(
        verbose_name=_("public ciblé pour la formation"), max_length=200
    )
    description = models.CharField(verbose_name=_("description courte"), max_length=300)
    duration = models.CharField(
        verbose_name=_("durée de la formation"),
        help_text=_("ex une journée, une heure..."),
        max_length=50,
    )
    file = models.ForeignKey(
        Document,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Document lié"),
        help_text=_("Ce document est ignoré si le lien externe est défini"),
    )
    is_available_soon = models.BooleanField(
        default=False,
        verbose_name=_("bientôt disponible"),
        help_text=_(
            "si cette case est cochée, la formation ne sera pas accessible, mais l'utilisateur sera informé de sa publication prochaine"
        ),
    )
    link = models.URLField(_("Lien externe"), blank=True, null=True)

    def __str__(self):
        return self.name
