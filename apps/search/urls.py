from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns("",
    url(r"^/$", "search.views.home", name="home"),
    url(r"^search/$", "search.views.search", name="search_url"),
)
