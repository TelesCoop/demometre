from typing import Dict, List

from django.apps import AppConfig
from django.conf import settings
from django.db import models
from django.db.models import ForeignKey
from django.utils.datastructures import ImmutableList
from django.utils.translation import gettext_lazy as _

POSSIBLE_ARGS = ["help_text", "max_length", "features", "to"]
NUMBER_LARGER_THAN_LOCALES_COUNT = 100


def add_translated_fields_to_model(
    model: models.Model,
    field_name: str,
    locales: List[str],
    field_order: Dict[str, float],
):
    """
    Add translated fields (named {field}_{locale}) to a model.
    The translated fields are created by copying the original field and some of its
    parameters.
    """
    if field_name == "explanatory":
        return

    for locale_ix, locale in enumerate(locales):
        translated_field_name = f"{field_name}_{locale}"
        original_field = model._meta.get_field(field_name)
        field_class = type(original_field)
        args = {
            key: value
            for key, value in original_field.__dict__.items()
            if key in POSSIBLE_ARGS
        }
        if issubclass(field_class, ForeignKey):
            args["on_delete"] = models.SET_NULL
            args["to"] = original_field.related_model
            args["related_name"] = f"{field_name}s_{locale}"
        model.add_to_class(
            translated_field_name,
            field_class(
                **args,
                blank=True,
                null=True,
                verbose_name=f"{_(original_field.verbose_name or field_name)} ({locale})",
            ),
        )
        field_order[translated_field_name] = (
            field_order[field_name] + locale_ix / NUMBER_LARGER_THAN_LOCALES_COUNT
        )


def replace_field_panels(model: models.Model, field_name: str, locales: List[str]):
    """
    Update the model's panels to include the translated fields,
    keeping the original order.
    """
    from wagtail.admin.panels import FieldPanel

    if panels := getattr(model, "panels", None):
        try:
            panel_index = [
                panel.field_name
                if isinstance(panel, FieldPanel)
                else "__not_field_panel"
                for panel in panels
            ].index(field_name)
        except ValueError:
            # field not in panels
            return
        model.panels = (
            model.panels[:panel_index]
            + [FieldPanel(f"{field_name}_{locale}") for locale in locales]
            + model.panels[panel_index + 1 :]
        )


class AuthConfig(AppConfig):
    name = "open_democracy_back"
    label = "open_democracy_back"
    verbose_name = "Démomètre"

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals  # noqa

        locales_for_translated_fields = settings.LOCALES_FOR_TRANSLATED_FIELDS

        # loop through all models, find models that inherit ModelWithTranslatedFields
        # and programmatically create the translated fields
        for model in self.get_models():
            if model._meta.model_name == "questionnairequestion":
                # QuestionnaireQuestion is a proxy models, translated fields are defined
                # in the Question model
                translated_fields = getattr(
                    self.get_model("Question"), "translated_fields", None
                )
            elif not (translated_fields := getattr(model, "translated_fields", None)):
                continue

            field_order: Dict[str, float] = {
                field.name: ix for ix, field in enumerate(model._meta.fields)
            }
            for field_name in translated_fields:
                # if the model is a proxy model, we don't want to change its fields
                if not model._meta.proxy:
                    add_translated_fields_to_model(
                        model, field_name, locales_for_translated_fields, field_order
                    )

                # replace field in model.panels for wagtail admin
                replace_field_panels(model, field_name, locales_for_translated_fields)

            # reorder fields so that translated fields are
            # in the same place as the original field
            model._meta.fields = sorted(
                model._meta.fields, key=lambda field: field_order[field.name]
            )
            model._meta.fields = ImmutableList(model._meta.fields)
