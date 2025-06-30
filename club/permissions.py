from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin)

class IsBoardMember(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                request.user.is_admin or request.user.is_board
            )
        )

class IsSimpleMember(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                request.user.is_admin or (
                    not request.user.is_board and not request.user.is_admin
                )
            )
        )

class IsFinanceLeader(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                request.user.is_admin or (
                    request.user.is_board and request.user.department == 'finance'
                )
            )
        )

class IsMarketingLeader(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                request.user.is_admin or (
                    request.user.is_board and request.user.department == 'marketing'
                )
            )
        )

class IsTechnicalTeamLeader(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                request.user.is_admin or (
                    request.user.is_board and request.user.department == 'technical_team'
                )
            )
        )

class IsVisualCreationLeader(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                request.user.is_admin or (
                    request.user.is_board and request.user.department == 'visual_creation'
                )
            )
        )

class IsERLeader(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                request.user.is_admin or (
                    request.user.is_board and request.user.department == 'er'
                )
            )
        )

class IsHRLeader(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                request.user.is_admin or (
                    request.user.is_board and request.user.department == 'hr'
                )
            )
        )


class IsSelfOrBoard(BasePermission):
    def has_permission(self, request, view):
        # Allow safe methods only if authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_board or obj == request.user