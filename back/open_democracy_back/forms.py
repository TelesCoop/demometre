from django import forms
from django.core.exceptions import ValidationError

from open_democracy_back.models import (
    QuestionRule,
    ProfileDefinition,
    ResponseChoice,
    Survey,
)
from open_democracy_back.models.representativity_models import (
    RepresentativityCriteriaRule,
)

GENERIC_RULE_FIELD = [
    "conditional_question",
    "response_choices",
    "numerical_operator",
    "numerical_value",
    "float_value",
    "boolean_response",
]


class GenericRuleForm(forms.ModelForm):
    class Meta:
        abstract = True

    response_choices = forms.ModelMultipleChoiceField(
        queryset=ResponseChoice.objects.none(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "vertical"}),
        required=False,
    )

    def clean(self):
        cd = self.cleaned_data
        if (cd["numerical_operator"] and not cd["numerical_value"]) or (
            not cd["numerical_operator"] and cd["numerical_value"]
        ):
            raise ValidationError(
                "numerical_operator and numerical_value must be defined together"
            )

        return cd


class QuestionRuleForm(GenericRuleForm):
    class Meta:
        model = QuestionRule
        fields = ["question"] + GENERIC_RULE_FIELD

    def __init__(self, *args, **kwargs):
        question = kwargs.pop("question")
        other_questions_list = kwargs.pop("other_questions_list")
        super().__init__(*args, **kwargs)
        self.fields["question"].initial = question
        self.fields["conditional_question"].queryset = other_questions_list


class ProfileDefinitionForm(GenericRuleForm):
    class Meta:
        model = ProfileDefinition
        fields = ["profile_type"] + GENERIC_RULE_FIELD

    def __init__(self, *args, **kwargs):
        profile_type = kwargs.pop("profile_type")
        questions_list = kwargs.pop("questions_list")
        super().__init__(*args, **kwargs)
        self.fields["profile_type"].initial = profile_type
        self.fields["conditional_question"].queryset = questions_list


class RepresentativityCriteriaRefiningForm(forms.ModelForm):
    class Meta:
        model = RepresentativityCriteriaRule
        fields = [
            "representativity_criteria",
            "response_choice",
            "ignore_for_acceptability_threshold",
            "totally_ignore",
        ]


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ["name", "survey_locality", "code"]
