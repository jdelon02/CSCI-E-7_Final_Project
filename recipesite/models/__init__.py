"""This is a docstring which describes the module"""
from django.db import models
# from django.contrib.auth.models import AbstractUser
from .user import User
from .ingredients import Ingredients
from .recipes import Recipes
from .steps import Steps
from .bookmarks import Bookmarks
from .userfollowing import UserFollowing
