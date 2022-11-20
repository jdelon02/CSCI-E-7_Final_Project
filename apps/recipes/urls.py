"""recipesite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
# Django imports
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views  # as auth_views

from apps.recipes.views import recipe_view, ingredients_view
from apps.recipes.views.recipe_view import RecipeCreateView, RecipeUpdateView, BookmarkListView, RecipeDetailView
from apps.recipes.views.ingredients_view import IngredientsCreateView


urlpatterns = [
    path("", recipe_view.Index.as_view(), name="index"),
    path('recipe/add/', recipe_view.RecipeCreateView.as_view(), name='recipeadd'),
    path('recipe/<int:pk>', recipe_view.RecipeDetailView.as_view(), name='recipedetail'),
    path('recipe/<int:pk>/edit', recipe_view.RecipeUpdateView.as_view(), name='recipeupdate'),
    path('recipe/', recipe_view.Index.as_view(), name='recipesearch'),
    path("bookmarks", recipe_view.BookmarkListView.as_view(), name="bookmarks"),

    # API Routes
    path("api/recipe/<int:recipe_id>", recipe_view.RecipeDetailView.like_button, name='like'),
    path("api/bookmark/<int:recipe_id>", recipe_view.BookmarkListView.save_button, name='save'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
