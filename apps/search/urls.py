from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns("search.views",
    url(r"^$", "home", name="home"),
    url(r"^search/$", "search", name="search_url"),
)
