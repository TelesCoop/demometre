from collections import Counter

from django.core.management import BaseCommand

from open_democracy_back.models import (
    Survey,
    Pillar,
    Marker,
    Criteria,
    Question,
    ProfilingQuestion,
    ProfileType,
    Role,
    AssessmentType,
)

LANGUAGE_TO_CHECK = "en"
BASE_LANGUAGE = "fr"

MISSING_TRANSLATIONS = Counter()


def check_missing_field(instance, field):
    if getattr(instance, f"{field}_{BASE_LANGUAGE}") and not getattr(
        instance, f"{field}_{LANGUAGE_TO_CHECK}"
    ):
        print(
            f"Missing translation for {field} in {instance.__class__.__name__}, pk {instance.pk}"
        )
        MISSING_TRANSLATIONS[f"{instance.__class__.__name__}.{field}"] += 1


def check_missing_fields(instance, model):
    for field in model.translated_fields:
        check_missing_field(instance, field)


class Command(BaseCommand):
    help = "Check missing translations"

    def handle(self, *args, **options):
        survey = Survey.objects.first()
        for pillar in survey.pillars.all():
            check_missing_fields(pillar, Pillar)
            for marker in pillar.markers.all():
                check_missing_fields(marker, Marker)
                for criteria in marker.criterias.all():
                    check_missing_fields(criteria, Criteria)
                    for question in criteria.questions.all():
                        check_missing_fields(question, Question)

        for question in survey.profiling_questions.all():
            check_missing_fields(question, ProfilingQuestion)

        for profile_type in ProfileType.objects.all():
            check_missing_fields(profile_type, ProfileType)

        for role in Role.objects.all():
            check_missing_fields(role, Role)

        for assessment_type in AssessmentType.objects.all():
            check_missing_fields(assessment_type, AssessmentType)

        print("\n")

        for key, value in MISSING_TRANSLATIONS.most_common():
            print(f"{key}: {value}")
