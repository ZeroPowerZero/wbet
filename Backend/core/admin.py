from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Item,Bid,ItemImage

@admin.register(User)
class UserModelAdmin(UserAdmin):
  model=User
  list_display=['id','email','name','is_active','is_superuser','is_staff','is_customer','is_seller']
  
  list_filter=['is_superuser']
  
  fieldsets=[
    ("User Credentials",{"fields":["email","password"]}),
    ("Personal Information",{"fields":["name","username","address"]}),
    ("Permissions",{"fields":["is_active","is_staff","is_superuser","is_customer","is_seller"]})
    
  ]
  search_fields=["email"]
  ordering=["email","id"]
  filter_horizontal=[]
  
  add_fieldsets = (
        (None, {
            
            'fields': ('email', 'name', 'password1', 'password2','username','address','is_active', 'is_staff', 'is_superuser', 'is_customer', 'is_seller'),
        }),
    )
  
@admin.register(Item)
class ItemModelAdmin(admin.ModelAdmin):
  model=Item
  list_display=['id','title','description','min_price','seller','is_sold','auction_end_time','winner']
  
  list_filter=['id']

  search_fields=["id"]
  ordering=["title","id"]
  filter_horizontal=[]
  
  add_fieldsets = (
        (None, {
            
            'fields': ('title','description','min_price','seller','is_sold','auction_end_time','winner'),
        }),
    )
  
@admin.register(Bid)
class BidModelAdmin(admin.ModelAdmin):
  model=Bid
  list_display=['id','item','bidder','bid_amount','bid_time']
  
  list_filter=['id']

  search_fields=["id"]
  ordering=["item","id"]
  filter_horizontal=[]
  
  add_fieldsets = (
        (None, {
            
            'fields': ('item','bidder','bid_amount','bid_time'),
        }),
    )
  
  
@admin.register(ItemImage)
class ImageModelAdmin(admin.ModelAdmin):
  model=Bid
  list_display=['id','item','image']
  
  list_filter=['id']

  search_fields=["id"]
  ordering=["item","id"]
  filter_horizontal=[]
  
  add_fieldsets = (
        (None, {
            
            'fields': ('item','image'),
        }),
    )