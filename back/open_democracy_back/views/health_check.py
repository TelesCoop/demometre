import time

import django
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    # make sure connection to database is working
    django.db.connection.ensure_connection()
    # there have been errors in the past on longer requests,
    # so also test longer requests
    time.sleep(2)

    return Response("OK")
