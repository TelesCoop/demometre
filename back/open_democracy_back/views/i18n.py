from django.conf import settings
from django.http import HttpResponse


def set_locale(_, locale):
    """
    View to set the language cookie so that the user's language preference is used
    for all subsequent requests.
    """
    response = HttpResponse()
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, locale)
    return response
