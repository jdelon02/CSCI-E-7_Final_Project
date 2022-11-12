"""This is a docstring which describes the module"""
from curses.ascii import US
from django.forms import CharField, ModelForm, Textarea
from django.forms import ModelForm
from recipesite.models import Steps


class StepForm(ModelForm):
    """This is a docstring which describes the module"""
    
    class Meta:
        """This is a docstring which describes the module"""
        model = Steps
        fields = ['step']

    # def __str__(self):
    #     return self['step']
    
    def __init__(self, *args, **kwargs):
        super(StepForm, self).__init__(*args, **kwargs)
                        
        self.fields['step'] = CharField(
                        widget=Textarea
                    )