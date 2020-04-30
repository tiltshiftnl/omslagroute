from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
from .statics import USER_TYPES, USER_TYPES_DICT
from django.db import models


class User(AbstractUser):
    user_types = [ut for ut in USER_TYPES if ut[0] in [1, 5, 6]]

    user_type = models.PositiveSmallIntegerField(
        verbose_name=_('Gebruiker type'),
        choices=user_types,
        default=6,
    )

    objects = UserManager()

    @property
    def name(self):
        if self.first_name and self.last_name:
            return '%s %s' % (
                self.first_name,
                self.last_name,
            )
        return self.username

    @property
    def user_type_value(self):
        return USER_TYPES_DICT[self.user_type]

    class Meta:
        verbose_name = _('Gebruiker')
        verbose_name_plural = _("Gebruikers")
