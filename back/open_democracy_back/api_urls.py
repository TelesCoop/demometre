from django.urls import path, include
from rest_framework import routers
from rest_framework.generics import ListAPIView

from open_democracy_back.views.animator_views import (
    CloseWorkshopView,
    FullWorkshopView,
    WorkshopParticipationResponseView,
    WorkshopParticipationView,
    WorkshopView,
)
from open_democracy_back.views.content_views import BlogPostView, ResourceView

from open_democracy_back.views.page_views import (
    AnimatorPageView,
    ContentPageView,
    EvaluationInitiationPageView,
    EvaluationQuestionnairePageView,
    HomePageView,
    ParticipationBoardPageView,
    ProjectPageView,
    ReferentialPageView,
    ResultsPageView,
    UsagePageView,
)
from open_democracy_back.views.participation_views import (
    ParticipationResponseView,
    ParticipationView,
    CompletedQuestionsParticipationView,
)
from open_democracy_back.views.representativity_views import (
    RepresentativityCriteriaView,
)
from open_democracy_back.views.setting_views import (
    ImportantPagesSettingsView,
    RGPDSettingsView,
    StructureSettingsView,
)
from .models import Training
from .serializers.training_serializers import TrainingSerializer

from .views.assessment_views import (
    AssessmentAddExpertView,
    AssessmentResponseView,
    AssessmentsView,
    CompletedQuestionsInitializationView,
    ExpertView,
    ZipCodeSurveysView,
    AssessmentScoreView,
    get_chart_data,
    AssessmentDocumentView,
)
from .views.i18n import set_locale
from .views.profiling_views import (
    ProfilingQuestionView,
    RoleView,
    ProfileTypeView,
)
from .views.questionnaire_views import (
    CriteriaView,
    MarkerView,
    PillarView,
    QuestionnaireQuestionView,
    SurveyView,
    DefinitionView,
)

router = routers.DefaultRouter()
router.register(r"home-pages", HomePageView, basename="HomePage")
router.register(r"referential-pages", ReferentialPageView, basename="ReferentialPage")
router.register(
    r"participation-board-pages",
    ParticipationBoardPageView,
    basename="ParticipationBoardPage",
)
router.register(r"results-pages", ResultsPageView, basename="ResultsPage")
router.register(r"usage-pages", UsagePageView, basename="UsagePage")
router.register(r"project-pages", ProjectPageView, basename="ProjectPage")
router.register(
    r"evaluation-initiation-pages",
    EvaluationInitiationPageView,
    basename="EvaluationInitiationPage",
)
router.register(
    r"evaluation-questionnaire-pages",
    EvaluationQuestionnairePageView,
    basename="EvaluationQuestionnairePage",
)
router.register(
    r"animator-pages",
    AnimatorPageView,
    basename="AnimatorPage",
)
router.register(
    r"content-pages",
    ContentPageView,
    basename="ContentPage",
)
router.register(
    r"important-pages-settings",
    ImportantPagesSettingsView,
    basename="ImportantPagesSettings",
)
router.register(r"rgpd-settings", RGPDSettingsView, basename="RGPDSettings")
router.register(
    r"structure-settings", StructureSettingsView, basename="StructureSettings"
)
router.register(r"blog-posts", BlogPostView, basename="BlogPost")
router.register(r"resources", ResourceView, basename="Resources")

router.register(r"participations", ParticipationView, basename="Participation")
router.register(
    r"participation-responses",
    ParticipationResponseView,
    basename="ParticipationResponse",
)
router.register(
    r"assessment-responses", AssessmentResponseView, basename="AssessmentResponse"
)
router.register(
    r"profiling-questions", ProfilingQuestionView, basename="ProfilingQuestion"
)
router.register(
    r"questionnaire-questions",
    QuestionnaireQuestionView,
    basename="QuestionnaireQuestion",
)
router.register(r"workshops", WorkshopView, basename="Workshop")
router.register(r"full-workshops", FullWorkshopView, basename="FullWorkshop")
router.register(r"experts", ExpertView, basename="experts")
router.register(r"assessments", AssessmentsView, basename="assessments")
router.register(
    r"assessment-documents", AssessmentDocumentView, basename="assessment-documents"
)
router.register("surveys", SurveyView, basename="surveys")
router.register("profile-types", ProfileTypeView, basename="profile-types")


urlpatterns = [
    path(
        "surveys/by-zip-code/<str:zip_code>/",
        ZipCodeSurveysView.as_view({"get": "list"}),
    ),
    path(
        "assessments/by-locality/",
        AssessmentsView.as_view({"get": "get_or_create"}),
        name="create-assessment",
    ),
    path("pillars/", PillarView.as_view({"get": "list"})),
    path(
        "pillars/<int:pk>/",
        PillarView.as_view({"get": "retrieve"}),
        name="pillars-detail",
    ),
    path("markers/", MarkerView.as_view({"get": "list"})),
    path("markers/<int:pk>/", MarkerView.as_view({"get": "retrieve"})),
    path("criterias/", CriteriaView.as_view({"get": "list"})),
    path("criterias/<int:pk>/", CriteriaView.as_view({"get": "retrieve"})),
    path("definitions/", DefinitionView.as_view({"get": "list"})),
    path("definitions/<int:pk>/", DefinitionView.as_view({"get": "retrieve"})),
    path("roles/", RoleView.as_view({"get": "list"})),
    path("", include(router.urls)),
    path(
        "representativity-criterias/",
        RepresentativityCriteriaView.as_view({"get": "list"}),
    ),
    path(
        "participations/<int:pk>/questions/completed/",
        CompletedQuestionsParticipationView.as_view(),
    ),
    path(
        "assessments/<int:assessment_id>/questions/completed/",
        CompletedQuestionsInitializationView.as_view(),
    ),
    path(
        "assessments/<int:assessment_id>/scores/",
        AssessmentScoreView.as_view(),
    ),
    path(
        "assessments/<int:assessment_id>/questions/<int:question_id>/chart-data/",
        get_chart_data,
    ),
    path(
        "assessments/<int:assessment_id>/add-expert/",
        AssessmentAddExpertView.as_view(),
    ),
    path(
        "workshops/<int:workshop_pk>/participation/",
        WorkshopParticipationView.as_view({"post": "create"}),
    ),
    path(
        "workshops/participation/<int:pk>/",
        WorkshopParticipationView.as_view({"delete": "destroy"}),
    ),
    path(
        "workshops/<int:workshop_pk>/participation/<int:participation_pk>/response/",
        WorkshopParticipationResponseView.as_view({"post": "create"}),
    ),
    path(
        "workshops/<int:workshop_pk>/closed/",
        CloseWorkshopView.as_view(),
    ),
    path(
        "trainings/",
        ListAPIView.as_view(
            queryset=Training.objects.all(), serializer_class=TrainingSerializer
        ),
        name="traning-list",
    ),
    path("set-locale/<str:locale>/", set_locale, name="set-locale"),
]
