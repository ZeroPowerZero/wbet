
from rest_framework import serializers
from .models import User, Item, Bid, ItemImage

# User Serializer for registration and displaying user info
class UserSerializer(serializers.ModelSerializer):
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model=User
    fields="__all__"
    extra_kwargs = {
            'password': {'write_only': True}
        }
  
  def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
  
  def create(self, validated_data):
        # Remove password2 because it's not needed by create_user
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)
# Serializer for item images
class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ['id', 'image']
        
# User login serilaizer
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


# Item Serializer with nested images
class ItemSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)
    winner = UserSerializer(read_only=True, allow_null=True)
    images = ItemImageSerializer(many=True,read_only=True)

    class Meta:
        model = Item
        fields = [
            'id', 'title', 'description', 'min_price', 'seller',
            'is_sold', 'auction_end_time', 'winner', 'images'
        ]

    def create(self, validated_data):
        
        images_data = validated_data.pop('images', [])
        # seller should be set from request user, not from client input
        seller = self.context['request'].user
        item = Item.objects.create(seller=seller, **validated_data)
        for image_data in images_data:
            ItemImage.objects.create(item=item, **image_data)
        return item



# Bid Serializer
class BidSerializer(serializers.ModelSerializer):
    bidder = UserSerializer(read_only=True)
    item = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Bid
        fields = ['id', 'item', 'bidder', 'bid_amount', 'bid_time']

    def create(self, validated_data):
        bidder = self.context['request'].user
        bid = Bid.objects.create(bidder=bidder, **validated_data)
        return bid