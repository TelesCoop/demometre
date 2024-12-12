from django.test import TestCase
from rest_framework.reverse import reverse
from wagtail.models import Locale

from open_democracy_back.factories import PillarFactory
from open_democracy_back.models import BlogPost, HomePage, Resource


class TestQuestionnaireI18n(TestCase):
    def set_locale_on_cookie(self, locale):
        self.client.get(reverse("set-locale", args=[locale]))

    def test_questionnaire_i18n(self):
        pillar = PillarFactory.create()
        pillar.description_fr = "French description"
        pillar.description_en = "English description"
        pillar.save()

        self.set_locale_on_cookie("fr")
        res = self.client.get(
            reverse("pillars-detail", args=[pillar.pk]),
        ).json()
        self.assertEqual(res["description"], "French description")
        self.set_locale_on_cookie("en")
        res = self.client.get(reverse("pillars-detail", args=[pillar.pk])).json()
        self.assertEqual(res["description"], "English description")

    def test_i18n_fallback_to_french(self):
        pillar = PillarFactory.create()
        pillar.description_fr = "French description"
        pillar.save()

        self.set_locale_on_cookie("en")
        res = self.client.get(
            reverse("pillars-detail", args=[pillar.pk]),
        ).json()
        self.assertEqual(res["description"], "French description")

    def test_set_language_cookie_en_on_profile(self):
        self.client.get(reverse("auth:auth_profile"), headers={"ACCEPT_LANGUAGE": "en"})
        self.assertEqual(
            self.client.cookies["django_language"].value,
            "en",
        )

    def test_set_language_cookie_fr_on_profile(self):
        self.client.get(reverse("auth:auth_profile"), headers={"ACCEPT_LANGUAGE": "fr"})
        self.assertEqual(
            self.client.cookies["django_language"].value,
            "fr",
        )


class TestHomePageI18n(TestCase):
    def set_locale_on_cookie(self, locale):
        self.client.get(reverse("set-locale", args=[locale]))

    def test_home_page_content(self):
        from open_democracy_back.views.page_views import refresh_locale_pk_per_locale

        self.set_locale_on_cookie("fr")
        en_locale = Locale.objects.create(language_code="en")
        fr_locale = Locale.objects.get(language_code="fr")
        refresh_locale_pk_per_locale()

        HomePage.objects.create(
            title="Home Page",
            path="path",
            tag_line="tag line",
            introduction="FR introduction",
            depth=0,
            locale=fr_locale,
        )
        HomePage.objects.create(
            title="Home Page",
            path="path-en",
            tag_line="tag line",
            introduction="EN introduction",
            depth=0,
            locale=en_locale,
        )
        BlogPost.objects.create(locale=fr_locale)
        Resource.objects.create(locale=en_locale)
        Resource.objects.create(locale=en_locale)
        res = self.client.get(reverse("HomePage-list")).json()
        self.assertEqual(res[0]["introduction"], "FR introduction")
        self.assertEqual(len(res[0]["blogPosts"]), 1)
        self.assertEqual(len(res[0]["resources"]), 0)
        self.set_locale_on_cookie("en")

        res = self.client.get(reverse("HomePage-list")).json()
        self.assertEqual(res[0]["introduction"], "EN introduction")
        self.assertEqual(len(res[0]["blogPosts"]), 0)
        self.assertEqual(len(res[0]["resources"]), 2)
