from collections import defaultdict
from typing import Dict, Callable

from django.db.models import Count, Q, F
from django.http import Http404
from django.utils import translation

from open_democracy_back.models import (
    ResponseChoice,
    Category,
    ClosedWithScaleCategoryResponse,
    AssessmentResponse,
    ParticipationResponse,
    Question,
)
from open_democracy_back.scoring import get_interval_average_values
from open_democracy_back.utils import QuestionType


def get_chart_data_objective_queryset(
    assessment_id, prefix_queryset="", exclude_empty_for_question_type=None
):
    prefix = f"{prefix_queryset}__" if prefix_queryset else ""

    to_return = {
        f"{prefix}answered_by__is_unknown_user": False,
        f"{prefix}assessment_id": assessment_id,
    }

    if exclude_empty_for_question_type:
        response_name = Question.RESPONSE_NAME_BY_QUESTION_TYPE[
            exclude_empty_for_question_type
        ]
        to_return[f"{prefix}{response_name}__isnull"] = False

    return to_return


def get_chart_data_subjective_queryset(assessment_id, prefix_queryset=""):
    prefix = f"{prefix_queryset}__" if prefix_queryset else ""

    return {
        f"{prefix}participation__user__is_unknown_user": False,
        f"{prefix}participation__assessment_id": assessment_id,
        f"{prefix}has_passed": False,
    }


def get_chart_data_of_boolean_question(question, assessment_id):
    if question.objectivity == "objective":
        base_count = "assessmentresponses"
        base_queryset = get_chart_data_objective_queryset(
            assessment_id, base_count, QuestionType.BOOLEAN.value
        )
    else:
        base_count = "participationresponses"
        base_queryset = get_chart_data_subjective_queryset(assessment_id, base_count)

    result = (
        Question.objects.filter(id=question.id)
        .annotate(
            count=Count(
                base_count,
                filter=Q(**base_queryset),
            ),
            true=Count(
                base_count,
                filter=Q(**base_queryset, **{f"{base_count}__boolean_response": True}),
            ),
            false=Count(
                base_count,
                filter=Q(**base_queryset, **{f"{base_count}__boolean_response": False}),
            ),
        )
        .get()
    )
    return {
        "true": {"label": "Oui", "value": result.true},
        "false": {"label": "Non", "value": result.false},
        "count": result.count,
    }


def get_chart_data_of_choice_question(question, assessment_id, choice_type):
    locale = translation.get_language()
    if question.objectivity == "objective":
        base_count = f"{choice_type}_assessmentresponses"
        role_count = base_count
        base_queryset = get_chart_data_objective_queryset(assessment_id, base_count)
    else:
        base_count = f"{choice_type}_participationresponses"
        role_count = f"{base_count}__participation__role__name_{locale}"
        base_queryset = get_chart_data_subjective_queryset(assessment_id, base_count)

    response_choices = ResponseChoice.objects.filter(question_id=question.id).annotate(
        count=Count(base_count, filter=Q(**base_queryset)),
    )
    response_choices_role_count = response_choices.annotate(
        role_name=F(role_count)
    ).annotate(
        count_by_role=Count("role_name", filter=Q(**base_queryset)),
    )

    question_roles = [getattr(role, f"name_{locale}") for role in question.roles.all()]

    data = {"value": {}, "role": {}}
    total_count = 0
    for response_choice in response_choices:
        data["value"][response_choice.id] = {
            "label": getattr(response_choice, f"response_choice_{locale}"),
            "value": response_choice.count,
        }
    for response_choice in response_choices_role_count:
        if response_choice.role_name not in question_roles:
            # we don't want to show roles that are not attached to the question
            # because they are not displayed to the frontend, so the totals would
            # be wrong (less than 100%)
            continue
        data["value"][response_choice.id][response_choice.role_name] = {
            "value": response_choice.count_by_role,
        }
        total_count += response_choice.count_by_role

    # count is not the number of answers, because an answer can count multiple times
    # if answered for multiple profiles
    # we also only count roles that are still attached to the question
    data["count"] = total_count
    return data


def get_chart_data_of_unique_choice_question(question, assessment_id):
    return get_chart_data_of_choice_question(question, assessment_id, "unique_choice")


def get_chart_data_of_multiple_choice_question(question, assessment_id):
    return get_chart_data_of_choice_question(question, assessment_id, "multiple_choice")


def get_chart_data_of_closed_with_scale_question(question, assessment_id):
    locale = translation.get_language()
    if question.objectivity == "objective":
        base_count = "assessment_response"
        role_count = base_count
        base_queryset = get_chart_data_objective_queryset(assessment_id, base_count)
        root_queryset = get_chart_data_objective_queryset(assessment_id)
        model = AssessmentResponse
    else:
        base_count = "participation_response"
        role_count = f"{base_count}__participation__role__name_{locale}"
        base_queryset = get_chart_data_subjective_queryset(assessment_id, base_count)
        root_queryset = get_chart_data_subjective_queryset(assessment_id)
        model = ParticipationResponse

    base_queryset[f"{base_count}__question_id"] = question.pk

    closed_with_scale_responses = ClosedWithScaleCategoryResponse.objects.filter(
        **base_queryset
    ).exclude(response_choice_id=None)
    result = closed_with_scale_responses.values(
        "category_id", "response_choice_id"
    ).annotate(count=Count("id"))
    result_by_category_id = defaultdict(dict)
    for item in result:
        result_by_category_id[item["category_id"]][item["response_choice_id"]] = item[
            "count"
        ]

    counts_by_category_response_choice_role = (
        closed_with_scale_responses.annotate(role_name=F(role_count))
        .values("category_id", "response_choice_id", "role_name")
        .annotate(count=Count("id"))
    )

    data = {
        "value": {},
        "count": model.objects.filter(**root_queryset, question_id=question.id).count(),
    }
    response_choices = ResponseChoice.objects.filter(question_id=question.id)
    for category in Category.objects.filter(question_id=question.id):
        data["value"][category.id] = {
            "label": getattr(category, f"category_{locale}"),
            "value": {},
        }
        for response_choice in response_choices:
            data["value"][category.id]["value"][response_choice.id] = {
                "label": getattr(response_choice, f"response_choice_{locale}"),
                "value": result_by_category_id[category.id].get(response_choice.id, 0),
            }
    for count_by_role in counts_by_category_response_choice_role:
        data["value"][count_by_role["category_id"]]["value"][
            count_by_role["response_choice_id"]
        ][count_by_role["role_name"]] = {
            "value": count_by_role["count"],
        }

    data["choices"] = {
        response_choice.id: {
            "label": getattr(response_choice, f"response_choice_{locale}")
        }
        for response_choice in ResponseChoice.objects.filter(question_id=question.id)
    }

    return data


LABEL_BY_QUESTION_TYPE = {
    QuestionType.PERCENTAGE.value: "Pourcentage moyen",
    QuestionType.NUMBER.value: "Valeure moyenne",
}


def get_chart_data_of_interval_question(question, assessment_id):
    label = LABEL_BY_QUESTION_TYPE[question.type]
    response_ranges_name = Question.RESPONSE_RANGES_BY_QUESTION_TYPE[question.type]

    if question.objectivity == "objective":
        base_queryset = get_chart_data_objective_queryset(assessment_id)
        model = AssessmentResponse
    else:
        base_queryset = get_chart_data_subjective_queryset(assessment_id)
        model = ParticipationResponse

    try:
        result = (
            get_interval_average_values(
                model.objects.filter(**base_queryset, question_id=question.id),
                question.type,
            )
            .annotate(count=Count("id"))
            .get()
        )
    except model.DoesNotExist:
        raise Http404(
            f"no corresponding response for model {model}, question {question.pk}, assessment {assessment_id}"
        )

    return {
        "value": {"label": label, "value": result["avg_value"]},
        "count": result["count"],
        "ranges": [
            {
                "id": response_range.id,
                "score": response_range.associated_score,
                "lower_bound": response_range.lower_bound,
                "upper_bound": response_range.upper_bound,
            }
            for response_range in getattr(question, response_ranges_name).all()
        ],
    }


CHART_DATA_FN_BY_QUESTION_TYPE: Dict[str, Callable] = {
    QuestionType.BOOLEAN.value: get_chart_data_of_boolean_question,  # type: ignore
    QuestionType.UNIQUE_CHOICE.value: get_chart_data_of_unique_choice_question,  # type: ignore
    QuestionType.MULTIPLE_CHOICE.value: get_chart_data_of_multiple_choice_question,  # type: ignore
    QuestionType.PERCENTAGE.value: get_chart_data_of_interval_question,  # type: ignore
    QuestionType.CLOSED_WITH_SCALE.value: get_chart_data_of_closed_with_scale_question,  # type: ignore
    QuestionType.NUMBER.value: get_chart_data_of_interval_question,  # type: ignore
}
