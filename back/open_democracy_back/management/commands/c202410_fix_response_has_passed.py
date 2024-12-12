from django.core.management import BaseCommand
from django.db.models import Q

from open_democracy_back.models import ParticipationResponse, AssessmentResponse


class Command(BaseCommand):
    help = "Fix Response.has_passed"

    def handle(self, *args, **options):
        qs = (
            ParticipationResponse.objects.filter(has_passed=True)
            .filter(
                Q(unique_choice_response__isnull=False)
                | Q(multiple_choice_response__isnull=False)
                | Q(boolean_response__isnull=False)
                | Q(percentage_response__isnull=True)
                | Q(number_response__isnull=True)
            )
            .distinct()
        )
        self.stdout.write(f"Found {qs.count()} responses to fix")
        updated = qs.update(has_passed=False)
        self.stdout.write(f"Updated {updated} responses")
        qs = (
            AssessmentResponse.objects.filter(has_passed=True)
            .filter(
                Q(unique_choice_response__isnull=False)
                | Q(multiple_choice_response__isnull=False)
                | Q(boolean_response__isnull=False)
                | Q(percentage_response__isnull=True)
                | Q(number_response__isnull=True)
            )
            .distinct()
        )
        print(f"Found {qs.count()} responses to fix")
        updated = qs.update(has_passed=False)
        print(f"Updated {updated} responses")
