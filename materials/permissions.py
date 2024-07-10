from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user == view.get_object().owner:
            return True


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="moderator").exists():
            return True
