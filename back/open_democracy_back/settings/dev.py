from .base import *  # noqa: F401,F403

import sys

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-35rbfpb*$*g#+za7iz0*w1+$80)@*le31f--mv3287c*th273p"

WAGTAILADMIN_BASE_URL = "http://localhost:8000"

FRONT_END_URL = "http://localhost:3000"
SESSION_COOKIE_SAMESITE = None
CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = ("http://localhost:3000",)
CSRF_TRUSTED_ORIGINS = ["http://localhost:3000"]


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "no-reply@telescoop.fr"

INSTALLED_APPS.append("django_extensions")  # noqa: F405
INSTALLED_APPS.append("debug_toolbar")  # noqa: F405

MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405
INTERNAL_IPS = ["127.0.0.1"]


class DisableMigrations:
    """Disable migrations for tests so that it's faster"""

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


if "test" in sys.argv[1:] or "jenkins" in sys.argv[1:]:
    MIGRATION_MODULES = DisableMigrations()
    # add test runner to add a Locale, otherwise tests crash
    TEST_RUNNER = "open_democracy_back.tests.runner_with_base_objects.MyTestRunner"
