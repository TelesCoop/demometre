from django.db.models import Q
from django.shortcuts import render

from open_democracy_back.models import Question
from open_democracy_back.utils import QuestionType


def range_error(question, attribute_name):
    ranges = []
    for range in getattr(question, attribute_name).all():
        if range.linearized_score is not None:
            continue
        ranges.append(range.boundaries)
    return ", ".join(ranges)


def get_percentage_range_line_error(question):
    return range_error(question, "percentage_ranges")


def get_number_range_line_error(question):
    return range_error(question, "number_ranges")


def get_response_choices_line_error(question):
    choices = []
    for response_choice in question.response_choices.all():
        if response_choice.linearized_score is not None:
            continue
        choices.append(response_choice.response_choice_fr)
    return ", ".join(choices)


MISSING_SCORE_MAP = {
    QuestionType.UNIQUE_CHOICE.value: get_response_choices_line_error,  # type: ignore
    QuestionType.MULTIPLE_CHOICE.value: get_response_choices_line_error,  # type: ignore
    QuestionType.CLOSED_WITH_SCALE.value: get_response_choices_line_error,  # type: ignore
    QuestionType.PERCENTAGE.value: get_percentage_range_line_error,  # type: ignore
    QuestionType.NUMBER.value: get_number_range_line_error,  # type: ignore
}


def anomaly(request):
    question_missing_scores = (
        (
            Question.objects.filter(profiling_question=False)
            .exclude(type=QuestionType.BOOLEAN)
            .filter(
                Q(
                    percentage_ranges__linearized_score__isnull=True,
                    type=QuestionType.PERCENTAGE,
                )
                | Q(
                    number_ranges__linearized_score__isnull=True,
                    type=QuestionType.NUMBER,
                )
                | Q(
                    response_choices__linearized_score__isnull=True,
                    type__in=[
                        QuestionType.UNIQUE_CHOICE,
                        QuestionType.MULTIPLE_CHOICE,
                        QuestionType.CLOSED_WITH_SCALE,
                    ],
                )
            )
        )
        .prefetch_related("percentage_ranges", "number_ranges", "response_choices")
        .distinct()
    )

    score_missing_list = []
    for question_missing_score in question_missing_scores:
        get_text_function = MISSING_SCORE_MAP[question_missing_score.type]
        score_missing_list.append(
            {
                "text": get_text_function(question_missing_score),
                "url": f"/admin/open_democracy_back/questionnairequestion/edit/{question_missing_score.id}/",
            }
        )

    questions_without_criteria = Question.objects.filter(
        criteria=None, profiling_question=False
    )
    questions_without_criteria_list = []
    for question_without_criteria in questions_without_criteria:
        questions_without_criteria_list.append(
            {
                "text": str(question_without_criteria),
                "url": f"/admin/open_democracy_back/questionnairequestion/edit/{question_without_criteria.id}/",
            }
        )

    return render(
        request,
        "admin/missing_score.html",
        {
            "score_missing_list": score_missing_list,
            "questions_without_criteria_list": questions_without_criteria_list,
        },
    )
