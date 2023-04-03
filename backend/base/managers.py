from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy

class BankUserManager(BaseUserManager):
    def create_user(self, username, password, role, **args):
        if not username:
            raise ValueError(gettext_lazy("The Email must be set"))
        # email = self.normalize_email(username)
        user = self.model(username=username, role=role, **args)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **args):
        args.setdefault("is_staff", True)
        args.setdefault("is_superuser", True)
        args.setdefault("is_active", True)
        args.setdefault('role', 3)
        return self.create_user(username, password, **args)
