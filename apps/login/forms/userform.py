"""This is a docstring which describes the module"""
from curses.ascii import US
from django.forms import ModelForm
from apps.login.models import User


class UserPostForm(ModelForm):
    """This is a docstring which describes the module"""
    
    class Meta:
        """This is a docstring which describes the module"""
        model = User
        fields = ['body']

    def __str__(self):
        return self.id