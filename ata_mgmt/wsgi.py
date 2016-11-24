"""
WSGI config for ata_mgmt project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""





import os, sys, site
sys.path.insert(0, os.path.dirname(__file__))


from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ata_mgmt.settings")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


application = get_wsgi_application()
