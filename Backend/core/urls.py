from django.contrib import admin
from django.urls import path
from core.views import UserRegistration,UserLogin,Seller,ItemList,ItemBids

urlpatterns = [
    path('register/',UserRegistration.as_view(),name="Registeration"),
    path('login/',UserLogin.as_view(),name="login"),
    path('sell/',Seller.as_view(),name="seller"),
    path('allitems/',ItemList.as_view(),name="allitem"),
    path('itembids/<int:item_id>/',ItemBids.as_view(),name="itembids"),
]