from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from profiles.models import prfl_profile
from .models import *
from .serializers import SearchFriendsProfileSerializer
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


import logging
logger_error = logging.getLogger('friends_log_file')
logger = logging.getLogger(__name__)

class SearchFriends(generics.ListAPIView):
    """
    Api to search friends with q / Implemented cache example
    Methods: GET
    URL : http://127.0.0.1:8000/friends/api/search-friends/?q=
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    api_views = ['GET']
    queryset = prfl_profile.objects.filter(active=1)
    serializer_class = SearchFriendsProfileSerializer
    search_fields = ('profile_name', 'user__first_name', 'user__last_name', 'user__username')
    filter_fields = ('profile_name', 'user__first_name', 'user__last_name', 'user__username')

    @method_decorator(cache_page(60*1))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

class AddFriends(APIView):
    """
    API to add friends.
    Methods: POST
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ''
    api_views = ['POST']
    '''
    {
        "profile_id":<pk of profile>
    }
    '''
    def post(self, request, format=None):
        try:
            profile_id = request.data.get('profile_id',None)
            print ("request.data",request.data)
            if profile_id :
                if (not int(request.user.user_profile.profile_id) == int(profile_id)) : 
                    instance = frnd_friends_mapping.objects.create(profile_id=request.user.user_profile)
                    instance.friends_id.add(profile_id)
                    instance.save()
                    return Response({'success': 'Friend successfully added.'}, status=status.HTTP_200_OK)
                else:
                    return Response({"error" : 'You can be your own friend.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error" : 'please select friend'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)