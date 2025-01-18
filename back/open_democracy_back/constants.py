from django.utils.translation import gettext_lazy as _

ASSESSMENT_DOCUMENT_CATEGORIES = {
    "assessment_reports": _("Rapports d'évaluation"),
    "other": _("Autres documents"),
    "invoices": _("Factures"),
}
ASSESSMENT_DOCUMENT_CATEGORIES_CHOICES = [
    (k, v) for k, v in ASSESSMENT_DOCUMENT_CATEGORIES.items()
]
