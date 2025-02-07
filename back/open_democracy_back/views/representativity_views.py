from django.db.models import Subquery
from rest_framework import mixins, viewsets

from open_democracy_back.models.representativity_models import (
    RepresentativityCriteria, AssessmentRepresentativityCriteriaRule,
)
from open_democracy_back.permissions import HasAssessmentWriteAccessForRepresentativityCriteriaRule
from open_democracy_back.querysets import assessments_by_user
from open_democracy_back.serializers.representativity_serializers import (
    RepresentativityCriteriaSerializer, AssessmentRepresentativityCriteriaRuleSerializer,
)


class RepresentativityCriteriaView(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = RepresentativityCriteriaSerializer
    queryset = RepresentativityCriteria.objects.all()


class AssessmentRepresentativityCriteriaRuleView(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = AssessmentRepresentativityCriteriaRule.objects.all()
    serializer_class = AssessmentRepresentativityCriteriaRuleSerializer

    def get_queryset(self):
        rq =  AssessmentRepresentativityCriteriaRule.objects.filter(
            assessment_representativity__assessment_id__in=Subquery(
                assessments_by_user(self.request.user).values("pk")))
        return rq
