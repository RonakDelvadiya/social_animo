from django.conf.urls import include, url
from .views import *

urlpatterns = [

    # Custom App URLs
    url(r'^api/user-regestration/', UserRegestration.as_view(),name='user_regestration'),
    url(r'^api/email-verification/', EmailVerification.as_view(),name='email_verification'),
]
