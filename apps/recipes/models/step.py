"""Data models."""
from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from django.db.models import (
    Model,
    CASCADE,
    ForeignKey,
    CharField,
)
from apps.recipes.models import Recipe

# TODO: Description Field to model, recipe.


class Step(Model):

    step = CharField(
        max_length=240
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='recipe_Steps',
        blank=True,
        null=True
    )

    class Meta:
        app_label = 'recipes'

    def __str__(self):
        return self.step
        # return str(self.name)
