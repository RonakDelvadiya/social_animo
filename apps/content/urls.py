from django.conf.urls import include, url
from .views import *

urlpatterns = [

    # Custom App URLs
    url(r'^api/pic-add-update/', PictureAddUpdate.as_view(),name='profile_pic_add_update'),
    url(r'^api/status-add-update/', StatusAddUpdate.as_view(),name='status_add_update'),
    url(r'^api/add-like/', AddLikes.as_view(),name='add_like'),
    url(r'^api/add-comment/', AddComments.as_view(),name='add_comments'),
]