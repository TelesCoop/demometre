from django.test import TestCase
from django.urls import reverse

from open_democracy_back.tests.utils import authenticate


class TestScoring(TestCase):
    @authenticate
    def test_edit_user(self):
        new_data = {"username": "new username", "email": "new@mail.com"}
        self.client.patch(
            reverse("auth:edit_user"),
            new_data,
            content_type="application/json",
        )
        data = self.client.get(reverse("auth:auth_profile")).json()
        self.assertEqual(data["username"], new_data["username"])
        self.assertEqual(data["email"], new_data["email"])
