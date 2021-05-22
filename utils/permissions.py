from rest_framework.permissions import BasePermission


class IsJournalist(BasePermission):
    message = "You must be a journalist to acccess this endpoint"

    def has_permission(self, request, view):

        user = request.user
        if user is not None and user.is_authenticated:
            return user.role == "JN"
        return False
