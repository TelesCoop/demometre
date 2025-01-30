from django.core.management.base import BaseCommand

from open_democracy_back.models import ParticipationResponse, AssessmentResponse


class Command(BaseCommand):
    help = "Clean old Assessment Responses"

    def handle(self, *args, **options):
        assessment_responses_to_change = AssessmentResponse.objects.filter(
            question__objectivity="subjective"
        )
        self.stdout.write(
            f"There is {assessment_responses_to_change.count()} assessment responses linked to subjective question"
        )
        for assessment_response in assessment_responses_to_change:
            self.stdout.write(
                f"Assessment response {assessment_response.id} in treatement"
            )
            user = assessment_response.answered_by
            assessment = assessment_response.assessment
            user_participation = user.participations.filter(
                assessment_id=assessment.id
            ).first()
            if user_participation:
                participation_response, _ = ParticipationResponse.objects.get_or_create(
                    question_id=assessment_response.question_id,
                    has_passed=assessment_response.has_passed,
                    unique_choice_response_id=assessment_response.unique_choice_response_id,
                    boolean_response=assessment_response.boolean_response,
                    percentage_response=assessment_response.percentage_response,
                    number_response=assessment_response.number_response,
                    participation_id=user_participation.id,
                )
            else:
                self.stdout.write("There is no participation for the user who respond")
            closed_with_scale_response_categories = (
                assessment_response.closed_with_scale_response_categories.all()
            )
            for (
                closed_with_scale_response_categorie
            ) in closed_with_scale_response_categories:
                if user_participation:
                    closed_with_scale_response_categorie.assessment_response = None
                    closed_with_scale_response_categorie.participation_response = (
                        participation_response
                    )
                    closed_with_scale_response_categorie.save()
                else:
                    closed_with_scale_response_categorie.delete()
            assessment_response.delete()
