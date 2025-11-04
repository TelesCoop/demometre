from django.conf import settings

country = settings.COUNTRY

if country == "FR":
    from .fr.epci import EPCI  # noqa: F401
elif country == "BE":
    from .be.communes import EPCI  # noqa: F401
else:
    raise NotImplementedError(f"Country {country} not implemented")
