import factory
from django.db import models

import open_democracy_back.models as democracy_models

DEFAULT_PAGE_FIELDS = [
    "id",
    "path",
    "depth",
    "numchild",
    "translation_key",
    "locale",
    "latest_revision",
    "live",
    "has_unpublished_changes",
    "first_published_at",
    "last_published_at",
    "live_revision",
    "go_live_at",
    "expire_at",
    "expired",
    "locked",
    "locked_at",
    "locked_by",
    "title",
    "draft_title",
    "slug",
    "content_type",
    "url_path",
    "owner",
    "seo_title",
    "show_in_menus",
    "search_description",
    "latest_revision_created_at",
    "alias_of",
    "page_ptr",
]


class PageFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    title = factory.Faker("sentence", nb_words=4)
    path = factory.Faker("slug")
    slug = factory.Faker("slug")


def make_page_declarations(model):
    """
    Fill values for all custom fields of a page model so that pages can be
    created quickly.
    """
    to_return = {
        "title": factory.Faker("sentence", nb_words=4),
        "slug": factory.Faker("slug"),
    }
    for field in model._meta.fields:
        if field.name in DEFAULT_PAGE_FIELDS:
            continue
        if not (
            isinstance(field, models.CharField) or isinstance(field, models.TextField)
        ):
            continue
        max_length = getattr(field, "max_length", 100) or 100
        to_return[field.name] = f"<{field.verbose_name[:max_length-2]}>"

    return to_return


HomePageFactory = factory.make_factory(
    democracy_models.HomePage, **make_page_declarations(democracy_models.HomePage)
)
UsagePageFactory = factory.make_factory(
    democracy_models.UsagePage, **make_page_declarations(democracy_models.UsagePage)
)
ReferentialPageFactory = factory.make_factory(
    democracy_models.ReferentialPage,
    **make_page_declarations(democracy_models.ReferentialPage),
)
ParticipationBoardPageFactory = factory.make_factory(
    democracy_models.ParticipationBoardPage,
    **make_page_declarations(democracy_models.ParticipationBoardPage),
)
ResultsPageFactory = factory.make_factory(
    democracy_models.ResultsPage, **make_page_declarations(democracy_models.ResultsPage)
)
ProjectPageFactory = factory.make_factory(
    democracy_models.ProjectPage, **make_page_declarations(democracy_models.ProjectPage)
)
EvaluationInitiationPageFactory = factory.make_factory(
    democracy_models.EvaluationInitiationPage,
    **make_page_declarations(democracy_models.EvaluationInitiationPage),
)
EvaluationQuestionnairePageFactory = factory.make_factory(
    democracy_models.EvaluationQuestionnairePage,
    **make_page_declarations(democracy_models.EvaluationQuestionnairePage),
)
AnimatorPageFactory = factory.make_factory(
    democracy_models.AnimatorPage,
    **make_page_declarations(democracy_models.AnimatorPage),
)
ContentPageFactory = factory.make_factory(
    democracy_models.ContentPage, **make_page_declarations(democracy_models.ContentPage)
)
