from django.core.management import BaseCommand

from open_democracy_back.models import Assessment


class Command(BaseCommand):
    help = "Clean representativities"

    def handle(self, *args, **options):
        wrong = 0
        for assessment in Assessment.objects.all():
            for representativity in assessment.representativities.all():
                if (
                    representativity.representativity_criteria.survey_locality
                    != assessment.survey.survey_locality
                ):
                    representativity.delete()
                    wrong += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted {wrong} representativities with the wrong survey_locality "
                f"match between assessment and representativity."
            )
        )
