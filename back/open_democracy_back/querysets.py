from django.utils import timezone

from django.db.models import Q

from open_democracy_back.models import Assessment, Participation


def assessments_by_user(user):
    return Assessment.objects.filter(
        Q(
            participations__in=Participation.objects.filter_available(
                user.id, timezone.now()
            )
        )
        | Q(initiated_by_user=user)
        | Q(experts=user),
    ).distinct()
