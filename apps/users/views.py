from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserRegestrationSerializer
from .models import *

from datetime import datetime, timedelta
import traceback

from social_animo.settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_HOST

import logging
logger_error = logging.getLogger('users_log_file')
logger = logging.getLogger(__name__)


class UserRegestration(APIView):
    """
    API to regester user.
    Methods: POST
    """
    api_views = ['POST']
    '''
    url : http://127.0.0.1:8000/users/api/user-regestration/
    {
        "username":,
        "first_name":,
        "last_name":,
        "email":,
        "password":
    }
    '''
    def post(self, request, format=None):
        try:
            data = request.data
            serializer = UserRegestrationSerializer(data=data)
            if serializer.is_valid() :
                serializer.save()
                return Response({'success': 'User regestered successfully'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            logger.error(str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EmailVerification(APIView):
    """
    API to verify email.
    Methods: POST
    """
    api_views = ['POST']
    '''
    url : http://127.0.0.1:8000/users/api/email-verification/
    --> Initial for send a mail
    {
        "email":
    }

    --->
    {
        "email":,
        "otp":
    }
    '''
    def post(self, request, format=None):
        try:
            email = request.data.get("email",None)
            otp = request.data.get("otp",None)
            if email and not otp:  
                '''
                Post email with random unique otp in db then send mail
                '''
                generated_otp = otp_genertor()
                acknowledgement = send_email_for_verification(generated_otp,email)
                print ("generated_otp",generated_otp)
                print ("acknowledgement",acknowledgement)
                if acknowledgement :
                    usr_email_verification.objects.create(email=email,generated_otp=generated_otp)
                    return Response({'success': 'otp has been sent on this email : %s.'%(email) }, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Please add your email again.'}, status=status.HTTP_400_BAD_REQUEST)
            elif email and otp :
                current_date_with_10_min_gap = datetime.utcnow() - timedelta(minutes=10) # 10 min timeout
                get_quesryset = usr_email_verification.objects.filter(email=email,generated_otp=otp)
                if get_quesryset.filter(created_at__gte=current_date_with_10_min_gap).exists() :
                    get_quesryset.delete() # delete verified data
                    return Response({'success': 'your email has been verified successfully.'}, status=status.HTTP_200_OK)
                elif get_quesryset.filter(created_at__lt=current_date_with_10_min_gap).exists() :
                    get_quesryset.delete() # delete unverified data
                    return Response({'error': 'otp timeout exccessed. please regenerate.'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'Please add your email again.'}, status=status.HTTP_400_BAD_REQUEST)
            else :
                return Response({"error" : "Please provide email."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(str(e))
            print (traceback.print_exc())
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)