from rest_framework.permissions import BasePermission
from ..models import BankUser

class AuthorizeProvider(BasePermission):
    edit_methods = ("GET", "POST", "DELETE", "PUT")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role is BankUser.PROVIDER


class AuthorizeCustomer(BasePermission):
    edit_methods = ("GET", "POST", "DELETE", "PUT")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role is BankUser.CUSTOMER


class AuthorizeEmployee(BasePermission):
    edit_methods = ("GET", "POST", "DELETE", "PUT")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role is BankUser.EMPLOYEE

class AuthorizeAdmin(BasePermission):
    edit_methods = ("GET", "POST", "DELETE", "PUT")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser
