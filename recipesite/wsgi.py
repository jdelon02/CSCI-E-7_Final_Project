import os
from django.core.wsgi import get_wsgi_application
"""
WSGI config for recipesite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.production")
application = get_wsgi_application()
