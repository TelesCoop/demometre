from rest_framework import mixins, viewsets

from open_democracy_back.models.representativity_models import (
    RepresentativityCriteria,
)
from open_democracy_back.serializers.representativity_serializers import (
    RepresentativityCriteriaSerializer,
)


class RepresentativityCriteriaView(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = RepresentativityCriteriaSerializer
    queryset = RepresentativityCriteria.objects.all()
