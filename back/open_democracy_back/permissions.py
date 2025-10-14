from rest_framework.permissions import BasePermission

from open_democracy_back.models import (
    AssessmentDocument,
    Assessment,
    AssessmentRepresentativityCriteriaRule,
)
from open_democracy_back.models.animator_models import Workshop
from open_democracy_back.querysets import assessments_by_user


class IsWorkshopExpert(BasePermission):
    """
    Allows access only to the workshop expert.
    """

    def has_permission(self, request, view):
        is_authenticated = bool(request.user and request.user.is_authenticated)
        if not is_authenticated:
            return False
        workshop_id = (
            request.data.get("workshop_id")
            or request.query_params.get("workshop_id")
            or view.kwargs.get("workshop_pk", None)
            or view.kwargs.get("pk", None)
        )
        is_expert = bool(Workshop.objects.get(id=workshop_id).animator == request.user)
        return is_expert


class HasWriteAccessOnAssessment(BasePermission):
    """
    Only allow read/write access to AssessmentDocuments to those who have write access
    on the assessment.
    """

    def has_object_permission(self, request, view, obj: AssessmentDocument):
        from open_democracy_back.serializers.assessment_serializers import (
            get_assessment_role,
            has_details_access,
        )

        user = request.user
        role = get_assessment_role(obj.assessment, user)
        return has_details_access(role)


class HasAssessmentWriteAccessForUpdate(BasePermission):
    """
    Only allow read/write access to AssessmentDocuments to those who have write access
    on the assessment.
    """

    def has_object_permission(self, request, view, obj: Assessment):
        if request.method != "PATCH" and view.action != "add_participative_processes":
            return True
        from open_democracy_back.serializers.assessment_serializers import (
            get_assessment_role,
            has_details_access,
        )

        user = request.user
        role = get_assessment_role(obj, user)
        return has_details_access(role)


class HasAssessmentWriteAccessForRepresentativityCriteriaRule(BasePermission):
    """
    Only allow read/write access to AssessmentDocuments to those who have write access
    on the assessment.
    """

    def has_object_permission(
        self, request, view, obj: AssessmentRepresentativityCriteriaRule
    ):
        from open_democracy_back.serializers.assessment_serializers import (
            get_assessment_role,
            has_details_access,
        )

        user = request.user
        role = get_assessment_role(obj.assessment_representativity.assessment, user)
        return has_details_access(role)

    def has_permission(self, request, view):
        if request.method not in ["POST", "PATCH", "PUT", "DELETE"]:
            return False
        is_authenticated = bool(request.user and request.user.is_authenticated)
        if not is_authenticated:
            return False

        assessment_representativity_id = (
            request.data.get("assessment_representativity_id")
            or request.query_params.get("assessment_representativity_id")
            or view.kwargs.get("assessment_representativity_id", None)
            or view.kwargs.get("assessment_representativity_id", None)
        )
        if assessment_representativity_id is None:
            return True
        return (
            assessments_by_user(request.user)
            .filter(representativities__id=assessment_representativity_id)
            .exists()
        )
