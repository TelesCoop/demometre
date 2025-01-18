import json
from collections import defaultdict
from django.shortcuts import render, redirect
from django.urls import reverse
from open_democracy_back.forms import (
    ProfileDefinitionForm,
    QuestionRuleForm,
    RepresentativityCriteriaRefiningForm,
    SurveyForm,
)
from django.db.models import Q
from django.views.generic.edit import BaseDeleteView

from open_democracy_back.models import (
    ProfileType,
    ProfilingQuestion,
    Question,
    QuestionnaireQuestion,
    QuestionType,
    ResponseChoice,
)
from open_democracy_back.models.questionnaire_and_profiling_models import (
    ProfileDefinition,
    QuestionRule,
    Survey,
)
from open_democracy_back.models.representativity_models import (
    RepresentativityCriteria,
    RepresentativityCriteriaRule,
)


def get_question_response_by_question_id(question_list):
    questions_response_by_question_id = defaultdict(
        lambda: {"type": "", "responses": {}}
    )
    for question in question_list:
        questions_response_by_question_id[question.id]["type"] = question.type
        for response_choice in question.response_choices.all():
            questions_response_by_question_id[question.id]["responses"][
                response_choice.id
            ] = response_choice.response_choice_fr
    return json.dumps(questions_response_by_question_id)


def get_data_for_creating_profile_definition(profile_type):
    data = {}
    data["questions_list"] = ProfilingQuestion.objects.filter(
        ~Q(type=QuestionType.CLOSED_WITH_SCALE)
    ).prefetch_related("response_choices")
    data["profile_type"] = profile_type
    data["rules"] = ProfileDefinition.objects.filter(profile_type_id=profile_type.id)
    data["rules_intersection_operator"] = profile_type.rules_intersection_operator
    data["questions_response_by_question_id"] = get_question_response_by_question_id(
        data["questions_list"]
    )
    return data


def get_data_for_creating_question_rules(question):
    data = {}
    data["is_profiling_question"] = question.profiling_question
    question_instance = (
        ProfilingQuestion if data["is_profiling_question"] else QuestionnaireQuestion
    )
    data["other_questions_list"] = question_instance.objects.filter(
        ~Q(id=question.id) & ~Q(type=QuestionType.CLOSED_WITH_SCALE)
    )
    if not data["is_profiling_question"]:
        data["other_questions_list"] = data["other_questions_list"].filter(
            criteria__marker__pillar=question.criteria.marker.pillar
        )
    data["other_questions_list"].prefetch_related("response_choices")
    data["question"] = question
    data["rules"] = QuestionRule.objects.filter(question_id=question.id)
    data["rules_intersection_operator"] = question.rules_intersection_operator
    data["questions_response_by_question_id"] = get_question_response_by_question_id(
        data["other_questions_list"]
    )
    return data


def create_question_rule_form(data):
    return QuestionRuleForm(
        question=data["question"],
        other_questions_list=data["other_questions_list"],
    )


def create_profile_definition_form(data):
    return ProfileDefinitionForm(
        profile_type=data["profile_type"],
        questions_list=data["questions_list"],
    )


def profile_intersection_operator_view(request, pk):
    profile_type = ProfileType.objects.get(id=pk)
    profile_type.rules_intersection_operator = request.POST.get("intersection-operator")
    profile_type.save()

    data = get_data_for_creating_profile_definition(profile_type)
    rule_form = create_profile_definition_form(data)

    return render(
        request,
        "admin/profile_definition.html",
        {
            "data": data,
            "rule_form": rule_form,
        },
    )


def question_intersection_operator_view(request, pk):
    question = Question.objects.get(id=pk)
    question.rules_intersection_operator = request.POST.get("intersection-operator")

    data = get_data_for_creating_question_rules(question)
    rule_form = create_question_rule_form(data)

    return render(
        request,
        "admin/question_rules.html",
        {
            "data": data,
            "rule_form": rule_form,
        },
    )


def hidrate_form_response_choices(request, rule_form):
    # The queryset of response_choices was changed dynamically un js, rule_form use the initial queryset, so the selection is not valid
    rule_form.fields["response_choices"].queryset = ResponseChoice.objects.filter(
        question_id=request.POST.get("conditional_question")
    )


def question_rules_view(request, pk):
    question = Question.objects.get(id=pk)
    data = get_data_for_creating_question_rules(question)

    if request.method == "POST":
        rule_form = QuestionRuleForm(
            request.POST,
            question=data["question"],
            other_questions_list=data["other_questions_list"],
        )

        if request.POST.get("conditional_question"):
            hidrate_form_response_choices(request, rule_form)

        if rule_form.is_valid():
            rule_form.save()
            # No redirection, the user can create several filters in a row
            rule_form = create_question_rule_form(data)

    else:
        rule_form = create_question_rule_form(data)

    return render(
        request,
        "admin/question_rules.html",
        {
            "data": data,
            "rule_form": rule_form,
        },
    )


def profile_definition_view(request, pk):
    profile_type = ProfileType.objects.get(id=pk)
    data = get_data_for_creating_profile_definition(profile_type)

    if request.method == "POST":
        rule_form = ProfileDefinitionForm(
            request.POST,
            profile_type=data["profile_type"],
            questions_list=data["questions_list"],
        )

        if request.POST.get("conditional_question"):
            hidrate_form_response_choices(request, rule_form)

        if rule_form.is_valid():
            rule_form.save()
            # No redirection, the user can create several filters in a row
            rule_form = create_profile_definition_form(data)

    else:
        rule_form = create_profile_definition_form(data)

    return render(
        request,
        "admin/profile_definition.html",
        {
            "data": data,
            "rule_form": rule_form,
        },
    )


def representativity_criteria_refining_view(request, pk):
    representativity_criteria = RepresentativityCriteria.objects.get(id=pk)
    data = {
        "representativity_criteria": representativity_criteria,
        "name": representativity_criteria.name,
    }
    rule_forms = []

    if request.method == "POST":
        rule = RepresentativityCriteriaRule.objects.get(
            response_choice_id=request.POST["response_choice"],
            representativity_criteria_id=request.POST["representativity_criteria"],
        )
        rule_form = RepresentativityCriteriaRefiningForm(request.POST, instance=rule)
        if rule_form.is_valid():
            rule_form.save()

    for (
        response_choice
    ) in representativity_criteria.profiling_question.response_choices.all():
        rule, _ = RepresentativityCriteriaRule.objects.get_or_create(
            response_choice=response_choice,
            representativity_criteria=representativity_criteria,
        )

        rule_forms.append(RepresentativityCriteriaRefiningForm(instance=rule))

    return render(
        request,
        "admin/representativity_criteria_refining.html",
        {
            "data": data,
            "rule_forms": rule_forms,
        },
    )


def duplicate_instance_and_set_foreign_key(
    instance_to_duplicate, foreign_key_name, new_foreign_key
):
    new_instance = instance_to_duplicate
    new_instance.id = None
    setattr(new_instance, foreign_key_name, new_foreign_key)
    new_instance.save()
    return new_instance


QUESTION_CHILDS_TO_DUPLICATE_BY_QUESTION_TYPE = {
    QuestionType.UNIQUE_CHOICE.value: ["response_choices"],
    QuestionType.MULTIPLE_CHOICE.value: ["response_choices"],
    QuestionType.BOOLEAN.value: [],
    QuestionType.PERCENTAGE.value: ["percentage_ranges"],
    QuestionType.NUMBER.value: ["number_ranges"],
    QuestionType.CLOSED_WITH_SCALE.value: ["response_choices", "categories"],
}


def duplicate_question(question_to_duplicate, criterion):
    if question_to_duplicate.profiling_question:
        return None

    duplicated_question_id = question_to_duplicate.id
    new_question = duplicate_instance_and_set_foreign_key(
        question_to_duplicate, "criteria", criterion
    )
    question_to_duplicate = Question.objects.get(id=duplicated_question_id)

    child_keys_to_duplicate = QUESTION_CHILDS_TO_DUPLICATE_BY_QUESTION_TYPE.get(
        question_to_duplicate.type, []
    )
    for child_key in child_keys_to_duplicate:
        for instance in getattr(question_to_duplicate, child_key).all():
            duplicate_instance_and_set_foreign_key(instance, "question", new_question)

    # foreign keys whose relations should stay the same
    for foreign_key in ["assessment_types", "roles", "profiles"]:
        for instance in getattr(question_to_duplicate, foreign_key).all():
            getattr(new_question, foreign_key).add(instance)

    return new_question


def duplicate_criterion(criterion_to_duplicate, marker):
    questions = list(criterion_to_duplicate.questions.all())
    new_criterion = duplicate_instance_and_set_foreign_key(
        criterion_to_duplicate, "marker", marker
    )

    for question in questions:
        duplicate_question(question, new_criterion)


def duplicate_marker(marker_to_duplicate, pillar):
    criteria = list(marker_to_duplicate.criterias.all())
    new_marker = duplicate_instance_and_set_foreign_key(
        marker_to_duplicate, "pillar", pillar
    )

    for criterion in criteria:
        duplicate_criterion(criterion, new_marker)


def duplicate_pillar(pillar_to_duplicate, survey):
    markers = list(pillar_to_duplicate.markers.all())
    new_pillar = duplicate_instance_and_set_foreign_key(
        pillar_to_duplicate, "survey", survey
    )

    for marker in markers:
        duplicate_marker(marker, new_pillar)


def duplicate_survey(data, survey_to_duplicate):
    pillars = survey_to_duplicate.pillars.all()

    survey = Survey.objects.create(
        name=data["name"],
        survey_locality=data["survey_locality"],
        code=data["code"],
        description=data["description"],
    )
    for pillar in pillars:
        duplicate_pillar(pillar, survey)

    return survey


def duplicates_survey_view(request, pk):
    survey_to_duplicate = Survey.objects.get(id=pk)
    if request.method == "POST":
        survey_form = SurveyForm(request.POST)
        new_survey = duplicate_survey(survey_form.data, survey_to_duplicate)
        return redirect(f"/admin/open_democracy_back/survey/edit/{new_survey.id}")

    return render(
        request,
        "admin/duplicates_survey.html",
        {
            "survey": survey_to_duplicate,
            "form": SurveyForm(),
        },
    )


class QuestionRuleView(BaseDeleteView):
    model = QuestionRule

    def get_object(self):
        return QuestionRule.objects.get(id=self.kwargs.get("rule_pk"))

    def get_success_url(self):
        return reverse("question-filter", kwargs={"pk": str(self.kwargs.get("pk"))})


class ProfileDefinitionView(BaseDeleteView):
    model = ProfileDefinition

    def get_object(self):
        return ProfileDefinition.objects.get(id=self.kwargs.get("rule_pk"))

    def get_success_url(self):
        return reverse(
            "profile-type-definition", kwargs={"pk": str(self.kwargs.get("pk"))}
        )
