"""This is a docstring which describes the module"""
from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from django.forms import ModelForm, inlineformset_factory, CharField, ChoiceField, Select
from recipesite.models.ingredients import Ingredients



class IngredientsForm(ModelForm):
    """This is a docstring which describes the module"""
    # name = CharField(
    # )
    
    class Meta:
        """This is a docstring which describes the module"""
        model = Ingredients
        fields = [
            'quantitywhole',
            'quantityfraction',
            'unitId',
            'name',
            'description',
        ]
        
    # def __str__(self):
    #     return self.name

    def __init__(self, *args, **kwargs):
        super(IngredientsForm, self).__init__(*args, **kwargs)
        UNITSTATUS = Choices(
            (None, 'Measurement'),
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
            (None, 'Quantity'),
            ('1/4', _('1/4')),
            ('1/3', _('1/3')),
            ('1/2', _('1/2')),
            ('2/3', _('2/3')),
            ('3/4', _('3/4')),
        )
        WHOLE = Choices(
            (None, 'Quantity'),
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
        self.fields['quantitywhole'] = ChoiceField(
            choices=WHOLE,
            label="Quantity",
            required=False
            )
        self.fields['quantityfraction'] = ChoiceField(
            choices=QUANTS,
            label="Partial",
            initial="Select",
            required=False
            )
        self.fields['unitId'] = ChoiceField(
            choices=UNITSTATUS,
            label="Measurement",
            required=False
            )