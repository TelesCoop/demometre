import os

from django.http import HttpResponse
from django.urls import path

from open_democracy_back.models import Assessment, Participation


def clean_data(request=None):
    if not os.environ.get("E2E_TESTS"):
        return HttpResponse("This command is only for e2e tests")
    Assessment.objects.all().delete()
    Participation.objects.all().delete()
    return HttpResponse("OK")


urlpatterns = [
    path("clean-data", clean_data, name="clean-data"),
]
