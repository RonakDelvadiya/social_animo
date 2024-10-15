from django.conf.urls import include, url
from .views import *


urlpatterns = [

    # Custom App URLs
    url(r'^api/add-friends/', AddFriends.as_view(),name='add_friends'),
    url(r'^api/search-friends/', SearchFriends.as_view(),name='search_friends')
]