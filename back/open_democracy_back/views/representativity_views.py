from django.db.models import Subquery
from rest_framework import mixins, viewsets

from open_democracy_back.models.representativity_models import (
    RepresentativityCriteria,
    AssessmentRepresentativityCriteriaRule,
)
from open_democracy_back.permissions import (
    HasAssessmentWriteAccessForRepresentativityCriteriaRule,
)
from open_democracy_back.querysets import assessments_by_user
from open_democracy_back.serializers.representativity_serializers import (
    RepresentativityCriteriaSerializer,
    AssessmentRepresentativityCriteriaRuleSerializer,
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
    viewsets.GenericViewSet,
):
    queryset = AssessmentRepresentativityCriteriaRule.objects.all()
    serializer_class = AssessmentRepresentativityCriteriaRuleSerializer
    permission_classes = [HasAssessmentWriteAccessForRepresentativityCriteriaRule]

    def get_queryset(self):
        return AssessmentRepresentativityCriteriaRule.objects.filter(
            assessment_representativity__assessment_id__in=Subquery(
                assessments_by_user(self.request.user).values("pk")
            )
        )
