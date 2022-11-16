"""recipesite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
# Django imports
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views # as auth_views

from .views import recipe_view, user_view, ingredients_view, scrape_view
from .views.recipe_view import RecipeCreateView, RecipeUpdateView, BookmarkListView, RecipeDetailView
from .views.ingredients_view import IngredientsCreateView
from .views.user_view import UserDetailView

urlpatterns = [
    # Examples:
    # url(r'^blog/', include('blog.urls', namespace='blog')),

    # provide the most basic login/logout functionality
    #url(r'^login/$', auth_views.LoginView.as_view(template_name='core/login.html'),
    #    name='core_login'),
    #url(r'^logout/$', auth_views.LogoutView.as_view(), name='core_logout'),

    # enable the admin interface
    # url(r'^admin/', admin.site.urls),
    path('admin/clearcache/', include('clearcache.urls')),
    path('admin/', admin.site.urls),
    
    
    path("", recipe_view.Index.as_view(), name="index"),
    path('recipe/add/', recipe_view.RecipeCreateView.as_view(), name='recipeadd'),
    path('recipe/<int:pk>', recipe_view.RecipeDetailView.as_view(), name='recipedetail'),
    path('recipe/<int:pk>/edit', recipe_view.RecipeUpdateView.as_view(), name='recipeupdate'),
    path('recipe/', recipe_view.Index.as_view(), name='recipesearch'),
    path("bookmarks", recipe_view.BookmarkListView.as_view(), name="bookmarks"),
    # path("scrape", scrape_view.Index, name='scrape'),
    # path('author/<int:pk>/delete/', recipe_view.RecipeDeleteView.as_view(), name='recipe-delete'),
    
    path('login/', user_view.login_view, name="login"),
    #path("login", auth_views.LoginView.as_view(template_name='core/login.html'), name='core_login'),
    path('logout', user_view.logout_view, name="logout"),
    #path("logout", auth_views.LogoutView.as_view(), name='core_logout'),

    path("register", user_view.register, name="register"),
    path("user/<int:pk>", user_view.UserDetailView.as_view(), name="user_detail"),
    # path("ingredients", ingredients_view.Index.as_view(), name="ingredients"),
    # path('ingredients/add/', IngredientsCreateView.as_view(), name='ingr-add'),
    
    path('', include('apps.scrape.urls')),
  
    
    
    # API Routes
    path("api/recipe/<int:recipe_id>",recipe_view.RecipeDetailView.like_button, name='like'),
    path("api/bookmark/<int:recipe_id>",recipe_view.BookmarkListView.save_button, name='save'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)