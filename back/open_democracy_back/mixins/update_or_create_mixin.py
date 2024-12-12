from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response


class UpdateOrCreateModelMixin(CreateModelMixin):
    """
    Update or create a model instance.
    Use `get_or_update_object` to retrieve the instance that you want to update.
    """

    def create(self, request, *args, **kwargs):
        try:
            instance = self.get_or_update_object(request, *args, **kwargs)
            serializer = self.get_serializer(instance, data=request.data)
            response_status = status.HTTP_200_OK
        except ObjectDoesNotExist:
            serializer = self.get_serializer(data=request.data)
            response_status = status.HTTP_201_CREATED
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=response_status, headers=headers)
