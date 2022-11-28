from django.contrib import admin
from apps.recipes.models import *

    
class RecipeIngredientInline(admin.StackedInline):
    model = Ingredient
    extra = 0
    fields = ['unitId', 'quantitywhole', 'quantityfraction', 'name', 'description']


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ['name', 'author']
    readonly_fields = ['timestamp', 'likes']
    raw_id_fields = ['author']
    
    
# Register your models here.

admin.site.register(Ingredient)
admin.site.register(Step)
admin.site.register(Recipe, RecipeAdmin)