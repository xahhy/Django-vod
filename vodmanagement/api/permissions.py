from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.models import AnonymousUser

class HasPermission(BasePermission):
    message = 'You must have permission of this video.'
    # my_safe_method = ['GET', 'PUT']
    # def has_permission(self, request, view):
    #     if request.method in self.my_safe_method:
    #         return True
    #     return False

    def has_object_permission(self, request, view, obj):
        #member = Membership.objects.get(user=request.user)
        #member.is_active
        print(request.user)
        permission = False
        if request.user.is_authenticated:
            permission = request.user.userpermission.has_permision()
        print(permission)
        return permission
        # if request.method in SAFE_METHODS:
        #     return True
        # return obj.user == request.user