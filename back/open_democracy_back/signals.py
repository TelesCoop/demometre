from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings

from open_democracy_back.models import Assessment


@receiver(pre_save, sender=Assessment)
def warn_when_assessment_is_closed(sender, instance, **kwargs):
    # send an email to DO when an assessment is closed (the end_date is set)
    # only when the end_date was not set yet
    try:
        former_instance = Assessment.objects.get(pk=instance.pk)
    except Assessment.DoesNotExist:
        return
    if not former_instance.end_date and instance.end_date:
        send_mail(
            "Cloture d'une évaluation",
            f"L'évaluation {instance.name} a été cloturée. "
            f"Cf https://demometre.org/admin/open_democracy_back/assessment/edit/{instance.pk}/",
            settings.DEFAULT_FROM_EMAIL,
            ["demometre@democratieouverte.org"],
        )
