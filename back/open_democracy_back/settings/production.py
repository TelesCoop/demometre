from .base import *  # noqa: F401,F403
import rollbar

DEBUG = False

SECRET_KEY = config.getstr("security.secret_key")  # noqa: F405
ALLOWED_HOSTS = config.getlist("security.allowed_hosts")  # noqa: F405
STATIC_ROOT = config.getstr("staticfiles.static_root")  # noqa: F405

# rollbar
MIDDLEWARE.append(  # noqa: F405
    "rollbar.contrib.django.middleware.RollbarNotifierMiddleware"
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config.getstr("database.name"),  # noqa: F405
        "USER": config.getstr("database.user"),  # noqa: F405
        "PASSWORD": config.getstr("database.password"),  # noqa: F405
    }
}

ROLLBAR = {
    "access_token": config.getstr("bugs.rollbar_access_token"),  # noqa: F405
    "environment": config.getstr("environment.environment", "production"),  # noqa: F405
    "root": BASE_DIR,  # noqa: F405
}

rollbar.init(**ROLLBAR)

ANYMAIL = {
    "MAILGUN_API_KEY": config.getstr("mail.api_key"),  # noqa: F405
    "MAILGUN_API_URL": "https://api.eu.mailgun.net/v3",
    "MAILGUN_SENDER_DOMAIN": "mail.telescoop.fr",
}
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
DEFAULT_FROM_EMAIL = "no-reply@telescoop.fr"
SERVER_EMAIL = "no-reply@telescoop.fr"

WAGTAILADMIN_BASE_URL = "https://demometre.org"
FRONT_END_URL = "https://demometre.org"

WAGTAIL_ENABLE_UPDATE_CHECK = False  # Disable update alerts
