from django.conf import settings

country = settings.COUNTRY

if country == "FR":
    from .fr.communes import COMMUNES  # noqa: F401
elif country == "BE":
    from .be.communes import COMMUNES  # noqa: F401
else:
    raise NotImplementedError(f"Country {country} not implemented")
