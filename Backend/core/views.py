from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import UserSerializer,UserLoginSerializer,UserProfileSerializer,ChangePasswordSerializer,SendPasswordToEmailSerializer,PasswordResetSerializer
from .models import User
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated


def get_tokens_for_user(user):
    if not user.is_active:
      raise AuthenticationFailed("User is not active")

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistration(APIView):
  #  renderer_classes=[UserRender,BrowsableAPIRenderer]
  
   def get(self,request):
    user=User.objects.all()
    serializer=UserSerializer(user,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)
   def post(self,request):
    serializer=UserSerializer(data=request.data)
    if serializer.is_valid():
      user=serializer.save()
      token=get_tokens_for_user(user)
      return Response({'token':token,"msg":"Registration Success"},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)