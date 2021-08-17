from rest_framework.permissions import BasePermission

from users.models import User


class AuthenticatedWithRole(BasePermission):
    """Allows authenticated uses with a specific role only."""

    role = User.ROLE

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == self.role and request.user.is_active == True


class ReadOnlyMixin(AuthenticatedWithRole):
    """
    Allows ready only access assistant users.
    """

    def has_permission(self, request, view):
        if request.method != "GET":
            return False
        return super().has_permission(request, view)


class IsAdminUser(AuthenticatedWithRole):
    """
    Allows access only to admin users.
    """

    role = User.Role.ADMIN


class IsUser(AuthenticatedWithRole):
    """
    Allows access only to dentist users.
    """

    role = User.Role.USER


# Read Only


class IsUserReadOnly(IsUser, ReadOnlyMixin):
    """
    Allows ready only access users.
    """

    pass

