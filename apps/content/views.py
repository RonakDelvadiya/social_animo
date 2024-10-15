from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .models import *
from .serializers import *
import traceback
import logging
logger_error = logging.getLogger('content_log_file')
logger = logging.getLogger(__name__)

class StatusAddUpdate(APIView):
    """
    API to add/update status.
    Methods: POST/PUT
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ''
    api_views = ['POST','PUT']

    '''
    {
        "status" :<char>,
    }
    '''
    def post(self, request, format=None):
        try:
            status_data = request.data.get('status',None)
            if status_data :
                cntnt_status.objects.create(profile=request.user.user_profile,status=status_data,created_by=request.user)
                return Response({'success': 'Status successfully added.'}, status=status.HTTP_200_OK)
            else:
                return Response({"error" : 'please add status.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

    '''
    {
        "status" :<char>,
        "status_id" : <pk>,
    }
    '''
    def put(self, request, format=None):
        try:
            status_id = request.data.get('status_id',None)
            status_data = request.data.get('status',None)
            if status_id and status_data :
                get_queryset = cntnt_status.objects.filter(status_id=status_id,profile=request.user.user_profile)
                if get_queryset.exists() :
                    get_queryset.update(status=status_data)
                    return Response({'success': 'Status updated successfully.'}, status=status.HTTP_200_OK)
                else:
                    return Response({"error" : 'status id is not available.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error" : 'please add status.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

class PictureAddUpdate(APIView):
    """
    API to add/update picture.
    Methods: POST/PUT
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ''
    api_views = ['POST','PUT']

    '''
    {
        "picture" :<file obj>,
        "is_current_profile_status":<send true if user change profile status else none>
    }
    '''
    def post(self, request, format=None):
        try:
            picture = request.data.get('picture',None)
            print ("request.data",request.data)
            if picture :
                is_current_profile_status = request.data.get('is_current_profile_status',None)
                if is_current_profile_status == 'true':
                    prfl_profile.objects.filter(profile_id=request.user.user_profile.profile_id).update(profile_picture=picture)
                cntnt_picture.objects.create(profile=request.user.user_profile,picture=picture,created_by=request.user)
                return Response({'success': 'Picture successfully added.'}, status=status.HTTP_200_OK)
            else:
                return Response({"error" : 'please select picture.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print (traceback.print_exc())
            logger.error(str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

    '''
    {
        "picture" :<char>,
        "picture_id" : <pk>,
    }
    '''
    def put(self, request, format=None):
        try:
            print ("request.data",request.data)
            picture_id = request.data.get('picture_id',None)
            picture = request.data.get('picture',None)
            print ("picture_id",picture_id)
            print ("picture",picture)
            if picture_id and picture :
                get_queryset = cntnt_picture.objects.filter(picture_id=picture_id,profile=request.user.user_profile.profile_id)
                if get_queryset.exists() :
                    print ("get_queryset",get_queryset)
                    result = get_queryset.update(picture=picture)
                    print ("result",result)
                    return Response({'success': 'Picture updated successfully.'}, status=status.HTTP_200_OK)
                else:
                    return Response({"error" : 'picture id is not available.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error" : 'please select picture.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AddLikes(APIView):
    """
    API to add likes on picture/comments/status.
    Methods: POST
    URL : http://127.0.0.1:8000/content/api/add-like/
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ''
    api_views = ['POST']
    
    '''
        {
            "picture" : <picture id> or "status" : <status id> or "comment" : <comment id>
        }
    '''
    @transaction.atomic
    def post(self, request, format=None):
        try:
            sid = transaction.savepoint()
            data = request.data
            picture_id = data.get('picture',None)
            status_id = data.get('status',None)
            comment_id = data.get('comment',None)
            
            if picture_id :
                if cntnt_likes.objects.filter(picture=picture_id,created_by=request.user) :
                    return Response({'error': 'You already Liked this picture.'}, status=status.HTTP_200_OK)
            if status_id :
                if cntnt_likes.objects.filter(status=status_id,created_by=request.user) :
                    return Response({'error': 'You already Liked this status.'}, status=status.HTTP_200_OK)
            if comment_id :
                if cntnt_likes.objects.filter(comment=comment_id,created_by=request.user) :
                    return Response({'error': 'You already Liked this comment.'}, status=status.HTTP_200_OK)

            add_serializer = AddLikesSerializer(data=data)
            data['created_by'] = request.user.id
            if add_serializer.is_valid() :
                add_serializer.save()
                return Response({'success': 'Successfully Liked.'}, status=status.HTTP_200_OK)
            else:
                transaction.savepoint_rollback(sid)
                return Response(add_serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            logger.error(str(e))
            transaction.savepoint_rollback(sid)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AddComments(APIView):
    """
    API to add comments on picture/other comments/status.
    Methods: POST
    URL : http://127.0.0.1:8000/content/api/add-comment/
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ''
    api_views = ['POST']
    
    '''
    {
        "picture" : <picture id> or "status" : <status id> or "parent_comment" : <comment id>,
        "comment" : <text field>
    }
    '''
    @transaction.atomic
    def post(self, request, format=None):
        try:
            sid = transaction.savepoint()
            data = request.data
            add_serializer = AddCommentsSerializer(data=data)
            data['created_by'] = request.user.id
            if add_serializer.is_valid() :
                add_serializer.save()
                return Response({'success': 'Successfully commented.'}, status=status.HTTP_200_OK)
            else:
                transaction.savepoint_rollback(sid)
                return Response(add_serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            logger.error(str(e))
            transaction.savepoint_rollback(sid)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)