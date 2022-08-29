from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from .managers import UserManager
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    phone_number = models.CharField(
        max_length=13,
        blank=True,
        validators=[RegexValidator(r"^010-?[1-9]\d{4}-?\d{4}$")],
    )
    point = models.IntegerField(default=0)
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    def __str__(self):
        return self.email
