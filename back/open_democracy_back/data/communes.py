from django.conf import settings

country = settings.COUNTRY

if country == "FR":
    from .fr.communes import COMMUNES
elif country == "BE":
    from .be.communes import COMMUNES
else:
    raise NotImplementedError(f"Country {country} not implemented")
