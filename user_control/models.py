from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)


ROLES = (('admin','admin'), ('creator','creator'), ('sale','sale'))
# Create your models here.
class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if not email:
            raise ValueError("email must be provided")
        if kwargs.get('is_staff') is not True:
            raise ValueError("is_staff must be True")
        if kwargs.get('is_superuser') is not True:
            raise ValueError("is_superuser must be True")

        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10,choices=ROLES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True)

    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ("created_at", )


class UserActivities(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name="user_activities", null=True,
        on_delete=models.SET_NULL
    )
    email = models.EmailField()
    fullname = models.CharField(max_length=50)
    action = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.fullname} {self.action} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"

