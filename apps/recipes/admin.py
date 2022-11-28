from django.contrib import admin
from django.contrib.auth import get_user_model
from apps.recipes.models import *

# Register your models here.

admin.site.register(Ingredient)
admin.site.register(Step)
admin.site.register(Recipe)
    
    
class RecipeIngredientInline(admin.StackedInline):
    model = Ingredient
    extra = 0
    fields = ['unitId', 'quantitywhole', 'quantityfraction', 'name', 'directions']


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ['name', 'author']
    readonly_fields = ['timestamp', 'likes']
    raw_id_fields = ['author']
    