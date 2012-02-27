#
# App: Search
# admin.py
#

from django.contrib import admin
from search.models import Query

admin.site.register(Query)
