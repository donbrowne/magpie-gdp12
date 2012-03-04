# coding: utf-8

# DJANGO IMPORTS
from django.conf import settings


# Admin Site Title
ADMIN_HEADLINE = getattr(settings, "GRAPPELLI_ADMIN_HEADLINE", 'Magpie Administration')
ADMIN_TITLE = getattr(settings, "GRAPPELLI_ADMIN_TITLE", 'Magpie site admin')

# Link to your Main Admin Site (no slashes at start and end)
ADMIN_URL = getattr(settings, "GRAPPELLI_ADMIN_URL", '/admin/')
