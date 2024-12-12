from django.utils import translation
from rest_framework import mixins, viewsets
from wagtail.models import Locale

from open_democracy_back.models.pages_models import (
    AnimatorPage,
    ContentPage,
    ParticipationBoardPage,
    EvaluationInitiationPage,
    EvaluationQuestionnairePage,
    HomePage,
    ProjectPage,
    ReferentialPage,
    ResultsPage,
    UsagePage,
)
from open_democracy_back.serializers.page_serializers import (
    AnimatorPageSerializer,
    ContentPageSerializer,
    ParticipationBoardPageSerializer,
    EvaluationInitiationPageSerializer,
    EvaluationQuestionnairePageSerializer,
    HomePageSerializer,
    ProjectPageSerializer,
    ReferentialPageSerializer,
    ResultsPageSerializer,
    UsagePageSerializer,
)


def refresh_locale_pk_per_locale():
    global locale_pk_per_locale
    locale_pk_per_locale = {
        locale.language_code: locale.pk for locale in Locale.objects.all()
    }


locale_pk_per_locale = {}
refresh_locale_pk_per_locale()


class OnlyPageInCurrentLanguageMixin:
    def get_queryset(self):
        language = translation.get_language()
        if pages_in_current_language := self.model.objects.filter(
            locale=locale_pk_per_locale[language]
        ):
            return pages_in_current_language
        return self.model.objects.all()


class HomePageView(
    OnlyPageInCurrentLanguageMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = HomePageSerializer
    model = HomePage


class UsagePageView(
    OnlyPageInCurrentLanguageMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UsagePageSerializer
    model = UsagePage


class ReferentialPageView(
    OnlyPageInCurrentLanguageMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ReferentialPageSerializer
    model = ReferentialPage


class ParticipationBoardPageView(
    OnlyPageInCurrentLanguageMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ParticipationBoardPageSerializer
    model = ParticipationBoardPage


class ResultsPageView(
    OnlyPageInCurrentLanguageMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ResultsPageSerializer
    model = ResultsPage


class ProjectPageView(
    OnlyPageInCurrentLanguageMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ProjectPageSerializer
    model = ProjectPage


class EvaluationInitiationPageView(
    OnlyPageInCurrentLanguageMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = EvaluationInitiationPageSerializer
    model = EvaluationInitiationPage


class EvaluationQuestionnairePageView(
    OnlyPageInCurrentLanguageMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = EvaluationQuestionnairePageSerializer
    model = EvaluationQuestionnairePage


class AnimatorPageView(
    OnlyPageInCurrentLanguageMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = AnimatorPageSerializer
    model = AnimatorPage


class ContentPageView(
    OnlyPageInCurrentLanguageMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ContentPageSerializer
    model = ContentPage
