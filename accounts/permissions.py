from rest_framework import permissions

class APIPermission(permissions.BasePermission):

    def has_permission(self,request,view):
        if request.method == 'POST':
            return True