from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from open_democracy_back.models import Survey
from open_democracy_back.models.questionnaire_and_profiling_models import (
    Criteria,
    Marker,
    Pillar,
    QuestionnaireQuestion,
    Definition,
)
from open_democracy_back.serializers.questionnaire_and_profiling_serializers import (
    CriteriaSerializer,
    MarkerSerializer,
    PillarSerializer,
    QuestionnaireQuestionSerializer,
    DefinitionSerializer,
    FullSurveySerializer,
)


class SurveyView(
    # mixins.RetrieveModelMixin,
    # mixins.ListModelMixin,
    viewsets.ModelViewSet,
):
    serializer_class = FullSurveySerializer
    queryset = (
        Survey.objects.prefetch_related("pillars")
        .prefetch_related("pillars__markers")
        .prefetch_related("pillars__markers__criterias")
        .prefetch_related("pillars__markers__criterias__questions")
        .prefetch_related("pillars__markers__criterias__questions__response_choices")
        .prefetch_related("pillars__markers__criterias__questions__percentage_ranges")
        .prefetch_related("pillars__markers__criterias__thematic_tags")
        .prefetch_related("pillars__markers__criterias__related_definition_ordered")
        .prefetch_related("pillars__markers__criterias")
    )

    @action(
        detail=False,
        methods=["GET"],
    )
    def all(self, request, *args, **kwargs):
        surveys = self.get_queryset()
        survey_serializer = self.get_serializer(
            surveys, many=True, context=self.get_serializer_context()
        )
        questions = (
            QuestionnaireQuestion.objects.exclude(criteria__marker__pillar__isnull=True)
            .prefetch_related("profiles")
            .prefetch_related("criteria")
            .prefetch_related("criteria__marker")
            .prefetch_related("criteria__marker__pillar")
            .prefetch_related("criteria__marker__pillar__survey")
            .prefetch_related("allows_to_explain")
            .prefetch_related("assessment_types")
            .prefetch_related("response_choices")
            .prefetch_related("categories")
            .prefetch_related("roles")
            .prefetch_related("rules")
            .prefetch_related("explained_by")
            .order_by(
                "criteria__marker__pillar__code",
                "criteria__marker__code",
                "criteria__code",
                "code",
            )
        )
        question_serializer = QuestionnaireQuestionSerializer(
            questions, many=True, context=self.get_serializer_context()
        )
        return Response(
            {
                "surveys": survey_serializer.data,
                "questions": question_serializer.data,
            }
        )


class PillarView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = PillarSerializer
    queryset = Pillar.objects.all()


class MarkerView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = MarkerSerializer
    queryset = Marker.objects.all()


class CriteriaView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = CriteriaSerializer
    queryset = Criteria.objects.all()


class QuestionnaireQuestionView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = QuestionnaireQuestionSerializer

    def get_queryset(self):
        return (
            QuestionnaireQuestion.objects.exclude(criteria__marker__pillar__isnull=True)
            .prefetch_related("profiles")
            .prefetch_related("criteria")
            .prefetch_related("criteria__marker")
            .prefetch_related("criteria__marker__pillar")
            .prefetch_related("criteria__marker__pillar__survey")
            .prefetch_related("allows_to_explain")
            .prefetch_related("assessment_types")
            .prefetch_related("response_choices")
            .prefetch_related("categories")
            .prefetch_related("roles")
            .prefetch_related("rules")
            .prefetch_related("explained_by")
            .order_by(
                "criteria__marker__pillar__code",
                "criteria__marker__code",
                "criteria__code",
                "code",
            )
        )


class DefinitionView(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Definition.objects.all()
    serializer_class = DefinitionSerializer
