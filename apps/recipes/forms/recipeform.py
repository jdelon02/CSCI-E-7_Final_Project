"""This is a docstring which describes the module"""
from django import forms
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from django.shortcuts import render
from django.urls import reverse_lazy
from django.forms import CharField, ModelForm, inlineformset_factory, ChoiceField, Select, Textarea
from apps.recipes.forms.ingredientform import IngredientForm
from apps.recipes.forms.stepform import StepForm
from apps.recipes.models import Recipe, Ingredient, Step
from easy_select2 import select2_modelform, Select2


class RecipeForm(ModelForm):
    """This is a docstring which describes the module"""
    QUANTS = Choices(
        ('1/4', _('1/4')),
        ('1/3', _('1/3')),
        ('1/2', _('1/2')),
        ('2/3', _('2/3')),
        ('3/4', _('3/4')),
    )

    class Meta:
        """This is a docstring which describes the module"""
        model = Recipe
        fields = [
            'name',
            'description',
            'prepHour',
            'prepMin',
            'cookHour',
            'cookMin',
            'skillLevel',
            'servingQuantity',
            'recipe_img'

        ]

    def __str__(self):
        return self.name

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

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)

        DIFFS = Choices(
            (None, 'Skill Level'),
            ('easy', _('Easy')),
            ('medium', _('Medium')),
            ('hard', _('Hard')),
        )
        SERVING = Choices(
            (None, 'Servings / Quantity'),
            ('2', _('2')),
            ('4', _('4')),
            ('6', _('6')),
            ('8', _('8')),
            ('8+', _('More than 8')),
        )
        HOURSTATUS = Choices(
            (None, 'Hours'),
            ('1', _('1')),
            ('2', _('2')),
            ('3', _('3')),
            ('4', _('4')),
            ('5', _('5')),
            ('6', _('6')),
            ('7', _('7')),
            ('8', _('8')),
            ('9', _('9')),
            ('10', _('10')),
            ('11', _('11')),
            ('12', _('12')),
        )
        MINSTATUS = Choices(
            (None, 'Minutes'),
            ('00', _('00')),
            ('15', _('15')),
            ('30', _('30')),
            ('45', _('45')),
        )
        self.fields['skillLevel'] = ChoiceField(
            choices=DIFFS,
            label="Skill Level",
            required=False,
            initial="Difficulty"

        )
        self.fields['servingQuantity'] = ChoiceField(
            choices=SERVING,
            label="Servings / Quantity",
            required=False
        )
        self.fields['prepHour'] = ChoiceField(
            choices=HOURSTATUS,
            label="Hours",
            required=False
        )
        self.fields['prepMin'] = ChoiceField(
            choices=MINSTATUS,
            label="Minutes",
            required=False
        )
        self.fields['cookHour'] = ChoiceField(
            choices=HOURSTATUS,
            label="Hours",
            required=False
        )
        self.fields['cookMin'] = ChoiceField(
            choices=MINSTATUS,
            label="Minutes",
            required=False
        )
        self.fields['description'] = CharField(
            widget=Textarea,
            label="Description*"
        )
        self.fields['name'] = CharField(
            label="Name*"
        )


IngredientFormSet = inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    extra=1,
    can_delete=True
)


def ingredientset_view(request):
    formset = IngredientFormSet(request.POST or None)

    if formset.is_valid():
        pass

    # return render(request, 'formset.html', {'formset': formset})
    return render(request, reverse_lazy('recipeupdate'), {'formset': formset})


StepFormSet = inlineformset_factory(
    Recipe,
    Step,
    form=StepForm,
    extra=1,
    can_delete=True
)


def stepformset_view(request):
    formset = StepFormSet(request.POST or None)

    if formset.is_valid():
        pass

    return render(request, reverse_lazy('recipeupdate'), {'formset': formset})
