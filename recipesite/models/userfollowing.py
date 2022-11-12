"""
This was what I ended up doing for follows.  
I think I should have done 2 foreign keys, 
but I remember the migration would not have run, 
it didn't like 2 foreign keys to same model.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from .user import User
from django.db.models import (
    Model,
    CASCADE,
    ForeignKey,
    ManyToManyField
)

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