"""
This was what I ended up doing for follows.  
I think I should have done 2 foreign keys, 
but I remember the migration would not have run, 
it didn't like 2 foreign keys to same model.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import (
    Model,
    CASCADE,
    ForeignKey,
    ManyToManyField
)

from apps.login.models.user import User


class UserFollowing(Model):
    follower = ForeignKey(
        User,
        on_delete=CASCADE
    )
    following = ManyToManyField(
        User,
        blank=True,
        related_name='following'
    )

    class Meta:
        app_label = 'login'
