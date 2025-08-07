from django.conf import settings

country = settings.COUNTRY

if country == "FR":
    from .fr.epci import EPCI
elif country == "BE":
    EPCI = []
else:
    raise NotImplementedError(f"Country {country} not implemented")
