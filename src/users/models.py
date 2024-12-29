from django.db import models
from django.contrib.auth import models as auth_models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserInfo(models.Model):
    user = models.OneToOneField(auth_models.User, related_name='info', on_delete=models.CASCADE)

    ejudge_user_id = models.PositiveIntegerField(
        help_text='Идентификатор пользователя в еджадже',
        default=0,
        blank=True,
    )
