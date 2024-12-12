from open_democracy_back.models import *
import django.apps
from django.db import models as django_models
from bs4 import BeautifulSoup


def is_one_of_subclasses(model, classes):
    for cls in classes:
        if issubclass(model, cls):
            return True
    return False


def count_words(string):
    return len([el for el in string.split(" ") if len(el)])


# count words in all pages
models = list(django.apps.apps.get_models())
word_count = 0
pages_res = []
for model in models:
    words_for_model = 0
    if not issubclass(model, Page):
        continue
    for field in model._meta.get_fields():
        if not is_one_of_subclasses(
            field.__class__, [StreamField, RichTextField, django_models.CharField]
        ):
            continue
        for instance in model.objects.filter(locale=1):
            text = getattr(instance, field.name)
            if issubclass(field.__class__, StreamField):
                text = BeautifulSoup(str(text), "html.parser").text
            wc = count_words(str(text or ""))
            pages_res.append(
                [
                    model._meta.model_name,
                    field.name,
                    text,
                    wc,
                ]
            )
            words_for_model += wc
    print(f"Model: {model.__name__}, Words: {words_for_model}")
    word_count += words_for_model

print("Total count for pages: ", word_count)

# count words in questionnaire
word_count = 0
questionnaires_res = []
for model in models:
    model_meta = model._meta
    words_for_model = 0
    if model._meta.model_name == "questionnairequestion":
        continue
    elif not (translated_fields := getattr(model, "translated_fields", None)):
        continue
    for instance in model.objects.all():
        for field in translated_fields:
            model_field = model_meta.get_field(field)
            text = getattr(instance, f"{field}_fr")
            if issubclass(model_field.__class__, StreamField):
                text = BeautifulSoup(str(text), "html.parser").text
            wc = count_words(str(text or ""))
            questionnaires_res.append(
                [
                    model._meta.model_name,
                    field,
                    text,
                    wc,
                ]
            )
            words_for_model += wc
    print(f"Model: {model.__name__}, Words: {words_for_model}")
    word_count += words_for_model

print("Total count for questionnaires: ", word_count)
