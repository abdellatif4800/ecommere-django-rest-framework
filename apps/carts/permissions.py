from rest_framework import permissions
from rest_framework.response import Response


class CustomerAccessPermission(permissions.BasePermission):
    message = "Adding customers not allowed."

    def has_permission(self, request, view):

        if request.headers["Authorization"]:

            return True
        return False
