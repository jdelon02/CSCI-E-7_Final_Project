from django.contrib import admin
from apps.recipes.models import *

# Register your models here.

admin.site.register(Ingredients)
admin.site.register(Steps)
admin.site.register(Recipes)
