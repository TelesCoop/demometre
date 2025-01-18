import logging
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.views import exception_handler
from enum import Enum

# Get an instance of a logger
logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code and the message code to the response.
    if response is not None:
        response.data["status_code"] = response.status_code
        logger.error(f"An error occured: {response.data}")
        if "detail" in response.data:
            if isinstance(response.data["detail"].code, dict):
                response.data["field"] = response.data["detail"].code["field"]
                response.data["message_code"] = response.data["detail"].code["code"]
            else:
                response.data["message_code"] = response.data["detail"].code
        else:
            response.data["message_code"] = "server_error"

    return response


class ValidationFieldError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid input."
    default_code = "invalid"

    def __init__(self, field, code=None, detail=None):
        code = {"field": field, "code": code}
        super().__init__(detail, code)


class ErrorCode(Enum):
    EMAIL_ALREADY_EXISTS = "email_already_exists"
    EMAIL_NOT_VALID = "email_not_valid"
    NO_EMAIL = "no_email"
    WRONG_PASSWORD_FOR_EMAIL = "wrong_password_for_email"
    WRONG_PASSWORD_RESET_KEY = "wrong_password_reset_key"
    PASSWORD_RESET_KEY_OUTDATE = "password_reset_key_outdate"
    ASSESSMENT_ALREADY_INITIATED = "assessment_already_initiated"
    EMAIL_NOT_CORRESPONDING_ASSESSMENT = "email_not_corresponding_assessment"
    INCORRECT_INITIATOR_ASSESSMENT = "incorrect_initiator_assessment"
    NO_ZIP_CODE_MUNICIPALITY = "no_zip_code_municipality"
    NO_ZIP_CODE_EPCI = "no_zip_code_epci"
    UNCORRECT_LOCALITY_TYPE = "uncorrect_locality_type"
    PARTICIPATION_ALREADY_EXISTS = "participation_already_exists"
    QUESTION_NOT_NEEDED = "question_not_needed"
    NEED_PARTICIPATION_RESPONSE = "need_participation_response"
    NEED_ASSESSMENT_RESPONSE = "need_assessment_response"
    USER_NOT_FOUND = "user_not_found"
    INVALID_EMAIL_SHAPE = "invalid_email_shape"
    CGV_MUST_BE_CONSENTED = "cgv_not_consented"
    CGU_MUST_BE_CONSENTED = "cgu_not_consented"
