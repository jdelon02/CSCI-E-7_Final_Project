"""Data models."""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from model_utils import Choices

from django.db.models import (
    Model,
    CASCADE,
    ForeignKey,
    IntegerField,
    TextField,
    CharField,
    FloatField
)
from apps.recipes.models import Recipe
from apps.recipes.utils import number_str_to_float


class Ingredient(Model):
    UNITSTATUS = Choices(
        ('cup', ('Cup')),
        ('tablespoon', ('Tablespoon')),
        ('teaspoon', ('Teaspoon')),
        ('pint', ('Pint')),
        ('quart', ('Quart')),
        ('ounce', ('Ounce')),
        ('dozen', ('Dozen')),
        ('can', ('Can')),
        ('bunch', ('Bunch')),
        ('whole', ('Whole')),
    )
    QUANTS = Choices(
        ('1/4', _('1/4')),
        ('1/3', _('1/3')),
        ('1/2', _('1/2')),
        ('2/3', _('2/3')),
        ('3/4', _('3/4')),
    )
    """Data model for user accounts."""
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='recipe_Recipes',
        blank=True,
        null=True
    )
    quantitywhole = CharField(
        max_length=2,
        blank=True,
        null=True
    )
    quantityfraction = CharField(
        max_length=8,
        choices=QUANTS,
        blank=True,
        null=True
    )
    quantityCalc = FloatField(
        blank=True,
        null=True
    )
    unitId = CharField(
        max_length=10,
        choices=UNITSTATUS
    )
    name = CharField(
        max_length=75
    )
    description = CharField(
        max_length=100,
        blank=True,
        null=True
    )
    order = IntegerField(
        blank=True,
        null=True
    )

    class Meta:
        app_label = 'recipes'

    def __str__(self):
        return self.name
        # return str(self.name)

    def save(self, *args, **kwargs):
        if self.quantitywhole is not None and self.quantityfraction is not None:
            qty = str(self.quantitywhole) + ' ' + self.quantityfraction
        if self.quantityfraction is not None and self.quantitywhole is None:
            qty = str(self.quantityfraction)
        else:
            qty = str(self.quantitywhole)
        qty_as_float, qty_as_float_success = number_str_to_float(qty)
        if qty_as_float_success:
            self.quantityCalc = qty_as_float
        super().save(*args, **kwargs)
