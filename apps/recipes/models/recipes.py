"""Data models."""
from django.db import models

from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from djangoformsetjs.utils import formset_media_js
from django.db.models import (
    Model,
    CASCADE,
    ForeignKey,
    TextField,
    ManyToManyField,
    CharField,
    DateTimeField,
    IntegerField,
    ImageField
)

# from apps.recipes.models import Ingredients
from apps.login.models import User

# TODO: Description Field to model, recipe.


class Recipes(Model):

    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    SERVING = Choices(
        (None, 'Your String For Display'),
        ('2', _('2')),
        ('4', _('4')),
        ('6', _('6')),
        ('8', _('8')),
        ('8+', _('More than 8')),
    )
    DIFFS = Choices(
        ('easy', _('Easy')),
        ('medium', _('Medium')),
        ('hard', _('Hard')),
    )
    MINSTATUS = Choices(
        ('00', _('00')),
        ('15', _('15')),
        ('30', _('30')),
        ('45', _('45')),
    )

    name = CharField(
        max_length=80
    )
    description = CharField(
        max_length=240
    )
    servingQuantity = CharField(
        max_length=15,
        choices=SERVING,
        blank=True,
        null=True
    )
    skillLevel = CharField(
        max_length=10,
        choices=DIFFS,
        blank=True,
        null=True
    )
    prepHour = IntegerField(
        default=0,
        choices=[(i, i) for i in range(1, 12)],
        blank=True,
        null=True
    )
    prepMin = CharField(
        max_length=7,
        choices=MINSTATUS,
        blank=True,
        null=True
    )
    cookHour = IntegerField(
        default=0,
        choices=[(i, i) for i in range(1, 12)],
        blank=True,
        null=True
    )
    cookMin = CharField(
        max_length=7,
        choices=MINSTATUS,
        blank=True,
        null=True
    )
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='author_User',
        blank=True,
        null=True
    )
    timestamp = DateTimeField(
        auto_now_add=True,
        blank=True
    )
    likes = ManyToManyField(
        User,
        blank=True,
        related_name='likes'
    )
    recipe_img = ImageField(
        default='post.jpeg',
        upload_to='images/'
    )

    class Meta:
        app_label = 'recipes'

    @property
    def total_likes(self):
        return self.likes.count()

    def serialize(self):
        return {
            "id": self.id,
            # Originally, I had user included, but serialization breaks with foreign keys.
            # "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes.count()
        }

    def __str__(self):
        return self.name
        # return str(self.id)

    def get_absolute_url(self):
        return reverse('recipedetail', kwargs={'pk': self.pk})
