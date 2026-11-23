from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission

class CheckStatus(BasePermission):
    def has_permission(self,request,view):
        if request.user.user_status == 'pro':
            return True
        else:
            return False

class CheckMovie(BasePermission):
    def has_object_permission(self,request,view, obj):
        if request.user.user_status == 'pro':
            return True
        elif request.user.user_status == 'simple'and obj.status_movie == 'simple':
            return True
        return False