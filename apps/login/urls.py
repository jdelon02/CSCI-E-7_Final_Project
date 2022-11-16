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

from apps.login.views import user_view
from apps.login.views.user_view import UserDetailView

urlpatterns = [
    path('login/', user_view.login_view, name="login"),
    path('logout', user_view.logout_view, name="logout"),
    path("register", user_view.register, name="register"),
    path("user/<int:pk>", user_view.UserDetailView.as_view(), name="user_detail"),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)