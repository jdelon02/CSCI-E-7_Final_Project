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

urlpatterns = [

    path('admin/clearcache/', include('clearcache.urls')),
    path('admin/', admin.site.urls),

    path('', include('apps.scrape.urls')),
    path('', include('apps.login.urls')),
    path('', include('apps.recipes.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
