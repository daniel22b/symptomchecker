from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["id","username", "email"]
        
class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id","first_name", "last_name", "gender", "street",
                   "city",
                 "postal_code", "phone_number","age"]