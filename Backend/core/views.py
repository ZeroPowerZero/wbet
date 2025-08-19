from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import *
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
# User login 

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

class UserLogin(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({
                    'status': False,
                    'message': 'Email is not registered'
                }, status=status.HTTP_404_NOT_FOUND)

            if not check_password(password, user.password):
                return Response({
                    'status': False,
                    'message': 'Incorrect password'
                }, status=status.HTTP_401_UNAUTHORIZED)

            token = get_tokens_for_user(user) #it generates both tokens access and refresh
            
            access_token=token['access']
            return Response({
                'status': True,
                'message': 'Login Success',
                'token': access_token
            }, status=status.HTTP_200_OK)

        # Serializer validation failed
        return Response({
            'status': False,
            'message': 'Invalid input',
            'errors': serializer.errors  # optional, for debugging
        }, status=status.HTTP_400_BAD_REQUEST)


        
        
class Seller(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # get all items for this seller
        items = Item.objects.filter(seller=request.user)
        serializer = ItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # create item + images
            return Response({"msg": "Item added"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# All items 
class ItemList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # get all items 
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ItemList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = Item.objects.filter(item=request.user)
        serializer = ItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)





class ItemBids(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users

    def get(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        bids = Bid.objects.filter(item=item).order_by('-bid_amount')  # highest bid first
        serializer = BidSerializer(bids, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, item_id):
     try:
        item = Item.objects.get(id=item_id)
     except Item.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    # Prevent duplicate bids by same user on same item
     if Bid.objects.filter(item=item, bidder=request.user).exists():
        return Response(
            {'error': 'You have already placed a bid on this item.'},
            status=status.HTTP_400_BAD_REQUEST
        )

     serializer = BidSerializer(data=request.data, context={'request': request})
     if serializer.is_valid():
        serializer.save(item=item)  # item is injected here from dynamic url
        return Response(serializer.data, status=status.HTTP_201_CREATED)
     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

