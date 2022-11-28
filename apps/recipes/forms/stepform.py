"""This is a docstring which describes the module"""
from curses.ascii import US
from django.forms import CharField, ModelForm, Textarea
from recipes.models import Step


class StepForm(ModelForm):
    """This is a docstring which describes the module"""

    class Meta:
        """This is a docstring which describes the module"""
        model = Step
        fields = ['step']

    # def __str__(self):
    #     return self['step']

    def __init__(self, *args, **kwargs):
        super(StepForm, self).__init__(*args, **kwargs)

        self.fields['step'] = CharField(
            widget=Textarea
        )
