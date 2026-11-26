from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    message = "Only the article author can change this story."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author_id == request.user.id or request.user.is_staff
