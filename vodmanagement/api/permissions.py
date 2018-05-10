from rest_framework.permissions import BasePermission


class HasPermission(BasePermission):
    message = 'You must have permission of this video.'

    def has_object_permission(self, request, view, obj):
        return True
        permission = False
        if request.user.is_authenticated:
            try:
                permission = request.user.userpermission.has_permision()
            except:
                pass
        return permission
