"""This is a docstring which describes the module"""
from django import forms
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render
from django.urls import reverse_lazy
from django.forms import Form, URLField

class ScrapeForm(Form):
    """This is a docstring which describes the module"""
    
    url = URLField(label='Your website', required=False)
    
    class Meta:
        """This is a docstring which describes the module"""
        
        fields = [
            'url'
            
        ]
    
    def __str__(self):
        return self.url