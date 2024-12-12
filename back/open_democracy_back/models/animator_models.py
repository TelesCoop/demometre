from django.db import models
from my_auth.models import User
from django.utils.translation import gettext_lazy as _

from open_democracy_back.models.utils import FrontendRichText


class Participant(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(_("email address"), blank=True, unique=True, null=True)


class Workshop(models.Model):
    animator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="workshops",
        limit_choices_to={"groups__name": "Experts"},
    )
    assessment = models.ForeignKey(
        "open_democracy_back.Assessment",
        on_delete=models.CASCADE,
        related_name="workshops",
    )
    closed = models.BooleanField(default=False)
    date = models.DateField(null=True, blank=True, verbose_name="Date")
    name = models.CharField(max_length=128, verbose_name="Nom", default="")
    place = models.CharField(max_length=80, null=True, blank=True)
    type = models.CharField(
        max_length=10,
        choices=[("assessment", _("évaluation")), ("results", _("résultats"))],
        default="assessment",
    )

    # details
    comments = FrontendRichText(verbose_name=_("commentaires"), blank=True, default="")
    context = FrontendRichText(verbose_name=_("contexte"), blank=True, default="")
    course = FrontendRichText(verbose_name=_("déroulé"), blank=True, default="")
    demometre_suggestions = FrontendRichText(
        verbose_name=_("suggestions démomètre"), blank=True, default=""
    )
    platform_suggestions = FrontendRichText(
        verbose_name=_("suggestions sur la plateforme"), blank=True, default=""
    )
    improvement_observations = FrontendRichText(
        verbose_name=_("remarques sur les mesures d'amélioration"),
        blank=True,
        default="",
    )
    objectives = FrontendRichText(verbose_name=_("objectifs"), blank=True, default="")
    result_observations = FrontendRichText(
        verbose_name=_("remarques sur les résultats"), blank=True, default=""
    )

    class Meta:
        verbose_name = _("Atelier")

    def __str__(self):
        return f"Atelier pour l'évaluation {self.assessment}, par {self.animator}, le {self.date}"
