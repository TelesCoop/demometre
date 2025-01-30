from django.db.models import Count
from django.templatetags.static import static
from django.urls import path, reverse
from django.utils.html import format_html_join
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.snippets import widgets as wagtailsnippets_widgets
from wagtail_modeladmin.helpers import ButtonHelper
from wagtail_modeladmin.helpers import PermissionHelper
from wagtail_modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
    ModelAdminGroup,
)

from my_auth.models import User
from open_democracy_back.models import (
    Assessment,
    Criteria,
    ProfileType,
    Question,
    Role,
    ThematicTag,
    Definition,
    Pillar,
    Marker,
    QuestionnaireQuestion,
    ProfilingQuestion,
    Region,
    Department,
    Municipality,
    EPCI,
    AssessmentDocument,
    Training,
    Survey,
)
from open_democracy_back.models.assessment_models import AssessmentType
from open_democracy_back.models.contents_models import (
    BlogPost,
    Feedback,
    Partner,
    Person,
    Resource,
)
from open_democracy_back.models.participation_models import Participation
from open_democracy_back.models.representativity_models import (
    RepresentativityCriteria,
)
from open_democracy_back.views.custom_admin_views import anomaly
from open_democracy_back.views.wagtail_rule_views import (
    question_intersection_operator_view,
    question_rules_view,
    QuestionRuleView,
    profile_intersection_operator_view,
    profile_definition_view,
    ProfileDefinitionView,
    representativity_criteria_refining_view,
    duplicates_survey_view,
)


class RulesButtonHelper(ButtonHelper):
    # Define classes for our button, here we can set an icon for example
    view_button_classnames = ["button-small", "icon", "icon-cogs"]

    def view_button(self, obj):
        # Define a label for our button
        if isinstance(obj, Question):
            text = "Condition d'affichage de la question"
            url = "/admin/question/" + str(obj.id) + "/rules/"
        if isinstance(obj, ProfileType):
            text = "Définir ce profil"
            url = "/admin/profile-type/" + str(obj.id) + "/rules/"
        if isinstance(obj, RepresentativityCriteria):
            text = "Affiner le critère de représentativité"
            url = "/admin/representativity-criteria/" + str(obj.id) + "/rules/"
        return {
            "url": url,
            "label": text,
            "classname": self.finalise_classname(self.view_button_classnames),
            "title": text,
        }

    def get_buttons_for_obj(
        self, obj, exclude=None, classnames_add=None, classnames_exclude=None
    ):
        """
        This function is used to gather all available buttons.
        We append our custom button to the btns list.
        """
        btns = super().get_buttons_for_obj(
            obj, exclude, classnames_add, classnames_exclude
        )
        if "view" not in (exclude or []):
            btns.append(self.view_button(obj))
        return btns


class SurveyButtonHelper(ButtonHelper):
    # Define classes for our button, here we can set an icon for example
    view_button_classnames = ["button-small", "icon", "icon-cogs"]

    def view_button(self, obj):
        # Define a label for our button
        text = "Dupliquer le questionnaire"
        url = "/admin/survey/" + str(obj.id) + "/duplicates/"
        return {
            "url": url,
            "label": text,
            "classname": self.finalise_classname(self.view_button_classnames),
            "title": text,
        }

    def get_buttons_for_obj(
        self, obj, exclude=None, classnames_add=None, classnames_exclude=None
    ):
        """
        This function is used to gather all available buttons.
        We append our custom button to the btns list.
        """
        btns = super().get_buttons_for_obj(
            obj, exclude, classnames_add, classnames_exclude
        )
        if "view" not in (exclude or []):
            btns.append(self.view_button(obj))
        return btns


@hooks.register("register_snippet_listing_buttons")
def snippet_listing_buttons(snippet, user, next_url=None):
    if isinstance(snippet, Question):
        yield wagtailsnippets_widgets.SnippetListingButton(
            "Condition d'affichage de la question",
            "/admin/question/" + str(snippet.id) + "/rules/",
            priority=10,
        )
    if isinstance(snippet, ProfileType):
        yield wagtailsnippets_widgets.SnippetListingButton(
            "Définir ce profil",
            "/admin/profile-type/" + str(snippet.id) + "/rules/",
            priority=10,
        )
    if isinstance(snippet, RepresentativityCriteria):
        yield wagtailsnippets_widgets.SnippetListingButton(
            "Affiner le critère de représentativité",
            "/admin/representativity-criteria/" + str(snippet.id) + "/rules/",
            priority=10,
        )
    if isinstance(snippet, Survey):
        yield wagtailsnippets_widgets.SnippetListingButton(
            "Dupliquer le questionnaire",
            "/admin/survey/" + str(snippet.id) + "/duplicates/",
            priority=10,
        )


@hooks.register("insert_editor_js", order=100)
def editor_js():
    js_files = []
    js_includes = format_html_join(
        "\n",
        '<script type="module" src="{0}"></script>',
        ((static(filename),) for filename in js_files),
    )

    return js_includes


class CanNotEditPermissionHelper(PermissionHelper):
    def user_can_edit_obj(self, user, obj):
        return False

    def user_can_create(self, user):
        return False


class FeedbackModelAdmin(ModelAdmin):
    model = Feedback
    menu_label = "Retour d'expérience"
    menu_icon = "user"
    add_to_settings_menu = False
    search_fields = "name"


class BlogPostModelAdmin(ModelAdmin):
    model = BlogPost
    menu_label = "Article de blog"
    menu_icon = "doc-full"
    add_to_settings_menu = False
    search_fields = "title"


class ResourcesModelAdmin(ModelAdmin):
    model = Resource
    menu_label = "Ressource"
    menu_icon = "doc-full"
    add_to_settings_menu = False
    search_fields = "title"


class PartnerModelAdmin(ModelAdmin):
    model = Partner
    menu_label = "Partenaire"
    menu_icon = "link"
    add_to_settings_menu = False
    search_fields = "name"


class PersonModelAdmin(ModelAdmin):
    model = Person
    menu_label = "Membres"
    menu_icon = "group"
    add_to_settings_menu = False
    search_fields = "name"


class ContentAdminGroup(ModelAdminGroup):
    menu_label = "Contenus"
    menu_order = 200
    menu_icon = "folder-inverse"
    items = (
        FeedbackModelAdmin,
        BlogPostModelAdmin,
        ResourcesModelAdmin,
        PartnerModelAdmin,
        PersonModelAdmin,
    )


class ThematicTagModelAdmin(ModelAdmin):
    model = ThematicTag
    menu_label = "Thématiques"
    menu_icon = "pilcrow"
    menu_order = 202
    form_fields_exclude = ("slug",)
    add_to_settings_menu = False
    search_fields = ("name",)


class DefinitionsModelAdmin(ModelAdmin):
    model = Definition
    menu_label = "Définitions"
    menu_icon = "openquote"
    menu_order = 204
    add_to_settings_menu = False
    search_fields = ("word",)


class SurveyModelAdmin(ModelAdmin):
    model = Survey
    menu_label = "Questionnaire"
    menu_icon = "folder-inverse"
    add_to_settings_menu = False
    search_fields = ("name",)
    button_helper_class = SurveyButtonHelper


class PillarModelAdmin(ModelAdmin):
    model = Pillar
    list_filter = ["survey__name"]
    menu_label = "Pilier"
    menu_icon = "folder-inverse"
    add_to_settings_menu = False
    search_fields = ("name", "code")


class MarkerModelAdmin(ModelAdmin):
    model = Marker
    menu_label = "Marqueur"
    menu_icon = "folder-inverse"
    add_to_settings_menu = False
    list_filter = [
        "pillar__survey__name",
        "pillar__name",
    ]
    search_fields = ("name", "concatenated_code", "pillar__name")
    ordering = ("concatenated_code",)


class CriteriaModelAdmin(ModelAdmin):
    model = Criteria
    menu_label = "Critère"
    menu_icon = "folder-inverse"
    add_to_settings_menu = False
    list_filter = ["marker__pillar__survey__name_fr", "marker__pillar__name"]
    search_fields = (
        "name_fr",
        "concatenated_code",
        "marker__name_fr",
        "marker__pillar__name",
    )
    ordering = ("concatenated_code",)


class QuestionnaireQuestionModelAdmin(ModelAdmin):
    model = QuestionnaireQuestion
    # Drawer question for questionnaire question is inactive
    # button_helper_class = RulesButtonHelper
    menu_label = "Question"
    menu_icon = "folder-inverse"
    add_to_settings_menu = False
    list_filter = [
        "criteria__marker__pillar__survey__name",
        "criteria__marker__pillar__name",
        "objectivity",
        "roles",
        "profiles",
        "type",
    ]
    search_fields = (
        "name",
        "question_statement",
        "concatenated_code",
        "criteria__name",
        "criteria__marker__name",
        "criteria__marker__pillar__name",
    )
    ordering = ("concatenated_code",)
    form_view_extra_js = ["js/questions.js"]


class SurveyAdminGroup(ModelAdminGroup):
    menu_label = "Questionnaire"
    menu_order = 206
    menu_icon = "list-ol"
    items = (
        SurveyModelAdmin,
        PillarModelAdmin,
        MarkerModelAdmin,
        CriteriaModelAdmin,
        QuestionnaireQuestionModelAdmin,
    )


class RoleModelAdmin(ModelAdmin):
    model = Role
    menu_label = "Rôle"
    menu_icon = "folder-inverse"
    add_to_settings_menu = False
    search_fields = ("name",)


class ProfileTypeModelAdmin(ModelAdmin):
    model = ProfileType
    button_helper_class = RulesButtonHelper
    menu_label = "Type de profil"
    menu_icon = "folder-inverse"
    add_to_settings_menu = False
    search_fields = ("name",)
    list_display = ("name_with_rules_count",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(rules_count=Count("rules"))


class ProfilingQuestionModelAdmin(ModelAdmin):
    model = ProfilingQuestion
    list_filter = ("surveys",)
    button_helper_class = RulesButtonHelper
    menu_label = "Question de profilage"
    menu_icon = "folder-inverse"
    add_to_settings_menu = False
    search_fields = ("name", "question_statement")
    form_view_extra_js = ["js/questions.js"]


class ProfilingAdminGroup(ModelAdminGroup):
    menu_label = "Profilage"
    menu_order = 208
    menu_icon = "group"
    items = (
        RoleModelAdmin,
        ProfileTypeModelAdmin,
        ProfilingQuestionModelAdmin,
    )


class RepresentativityModelAdmin(ModelAdmin):
    model = RepresentativityCriteria
    button_helper_class = RulesButtonHelper
    menu_label = "Représentativité"
    menu_icon = "password"
    menu_order = 210
    add_to_settings_menu = False
    search_fields = ("name",)
    list_filter = ("survey_locality",)


class CanNotCreatePermissionHelper(PermissionHelper):
    def user_can_create(self, user):
        return False


class CanNotDeletePermissionHelper(PermissionHelper):
    def user_can_delete_obj(self, user, _):
        return False


class CanNotCreateOrDeletePermissionHelper(
    CanNotCreatePermissionHelper, CanNotDeletePermissionHelper
):
    pass


class AssessmentTypeModelAdmin(ModelAdmin):
    model = AssessmentType
    menu_label = "Type d'Évaluation"
    menu_icon = "folder-inverse"
    add_to_settings_menu = False
    permission_helper_class = CanNotCreateOrDeletePermissionHelper


class AssessmentModelAdmin(ModelAdmin):
    model = Assessment
    menu_label = "Évaluation"
    menu_icon = "date"
    add_to_settings_menu = False
    search_fields = ("municipality__name", "epci__name")
    form_view_extra_js = ["js/assessments.js"]


class AssessmentDocumentModelAdmin(ModelAdmin):
    model = AssessmentDocument
    menu_label = "Document d'évaluation"
    menu_icon = "doc-full"
    add_to_settings_menu = False


class ParticipationModelAdmin(ModelAdmin):
    model = Participation
    menu_label = "Participations aux évaluations"
    menu_icon = "user"
    add_to_settings_menu = False
    search_fields = (
        "user__username",
        "assessment__municipality__name",
        "assessment__epci__name",
    )
    permission_helper_class = CanNotEditPermissionHelper


class AssessmentAdminGroup(ModelAdminGroup):
    menu_label = "Évaluations"
    menu_order = 212
    menu_icon = "date"
    items = (
        AssessmentTypeModelAdmin,
        AssessmentModelAdmin,
        ParticipationModelAdmin,
    )


class RegionModelAdmin(ModelAdmin):
    model = Region
    menu_label = "Régions"
    menu_icon = "folder-inverse"
    add_to_settings_menu = False
    search_fields = ("name",)


class DepartmentModelAdmin(ModelAdmin):
    model = Department
    menu_label = "Départements"
    menu_icon = "folder-inverse"
    add_to_settings_menu = False
    search_fields = ("name", "code")


class CommuneModelAdmin(ModelAdmin):
    model = Municipality
    menu_label = "Communes"
    menu_icon = "folder-inverse"
    add_to_settings_menu = False
    search_fields = ("name",)


class EPCIModelAdmin(ModelAdmin):
    model = EPCI
    menu_label = "Intercommunalités"
    menu_icon = "folder-inverse"
    add_to_settings_menu = False
    search_fields = ("name",)


class LocalityAdminGroup(ModelAdminGroup):
    menu_label = "Localités"
    menu_order = 214
    menu_icon = "home"
    items = (
        RegionModelAdmin,
        DepartmentModelAdmin,
        CommuneModelAdmin,
        EPCIModelAdmin,
    )


@modeladmin_register
class TrainingAdmin(ModelAdmin):
    model = Training
    menu_order = 213
    menu_icon = "group"
    search_fields = ("name",)


class ExpertsAdmin(ModelAdmin):
    model = User
    menu_label = "Experts"
    menu_icon = "user"
    menu_order = 205
    add_to_settings_menu = True
    exclude_from_explorer = True
    list_display = (
        "username",
        "email",
        "last_login",
    )
    search_fields = ("username", "email")
    permission_helper_class = CanNotEditPermissionHelper

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only show admin user
        return qs.filter(groups__name="Experts")


modeladmin_register(ContentAdminGroup)
modeladmin_register(ThematicTagModelAdmin)
modeladmin_register(DefinitionsModelAdmin)
modeladmin_register(SurveyAdminGroup)
modeladmin_register(ProfilingAdminGroup)
modeladmin_register(RepresentativityModelAdmin)
modeladmin_register(LocalityAdminGroup)
modeladmin_register(AssessmentAdminGroup)
modeladmin_register(ExpertsAdmin)


@hooks.register("register_admin_urls")
def register_custom_admin_views():
    return [
        # Rules
        path(
            "question/<int:pk>/edit-intersection-operator/",
            question_intersection_operator_view,
            name="question-intersection-operator",
        ),
        path(
            "question/<int:pk>/rules/",
            question_rules_view,
            name="question-filter",
        ),
        path(
            "question/<int:pk>/rule/<int:rule_pk>/delete",
            QuestionRuleView.as_view(),
            name="delete-question-filter",
        ),
        path(
            "profile-type/<int:pk>/edit-intersection-operator/",
            profile_intersection_operator_view,
            name="profile-type-intersection-operator",
        ),
        path(
            "profile-type/<int:pk>/rules/",
            profile_definition_view,
            name="profile-type-definition",
        ),
        path(
            "profile-type/<int:pk>/rule/<int:rule_pk>/delete",
            ProfileDefinitionView.as_view(),
            name="delete-profile-type-definition",
        ),
        path(
            "representativity-criteria/<int:pk>/rules/",
            representativity_criteria_refining_view,
            name="representativity-criteria-refining",
        ),
        # Anomaly
        path("anomaly/", anomaly, name="anomaly"),
        path(
            "survey/<int:pk>/duplicates/",
            duplicates_survey_view,
            name="duplicates-survey",
        ),
    ]


@hooks.register("register_admin_menu_item")
def register_missing_score_item():
    return MenuItem("Anomalies", reverse("anomaly"), icon_name="warning")
