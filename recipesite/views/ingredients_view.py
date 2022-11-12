"""This is a docstring which describes the module"""
import json
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.serializers import serialize
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
from django.forms import formset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from ..models import *
from ..forms import ingredientsform, recipesform
# from recipesite.forms.recipesform import IngredientFormSet, RecipesForm

class Index(ListView):
    """This is a docstring which describes the module"""
    model = Ingredients
    context_object_name = 'ingredients_listview'
    template_name = 'recipesite/ingredients_list.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(Index,
                        self).get_context_data(*args, **kwargs)
        current_user = self.request.user.id
        context['currentUser'] = current_user
        
        return context
    

class IngredientsCreateView(CreateView):
    model = Ingredients
    form_class = ingredientsform.IngredientsForm
    template_name = 'recipesite/ingredients_form.html'