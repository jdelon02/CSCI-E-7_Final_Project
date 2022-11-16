"""This is a docstring which describes the module"""
from django.db import models
from django.db.models import (
    Model,
    CASCADE,
    ForeignKey
)
from apps.login.models import User
from recipesite.models import Recipes

class Bookmarks(Model):
    user = ForeignKey(
        User, 
        on_delete=CASCADE
    )
    recipes = ForeignKey(
        Recipes, 
        on_delete=CASCADE,
        related_name='recipes'
    )

    class Meta:
        app_label = 'login' 
        
    def __str__(self):
        return str(self.id)