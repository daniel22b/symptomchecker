from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile, Disease


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]
        extra_kwargs = {"password": {"write_only": True}}


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    disease = serializers.SlugRelatedField(queryset = Disease.objects.all(),
                                           slug_field = "name",
                                            allow_null = True)
    
    class Meta:

        model = UserProfile
        fields = ["id","user","first_name", "last_name",
                   "gender", "street", "city",
                 "postal_code", "phone_number","age","disease"]
    
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)

        if self.instance:
            self.fields["user"] = UserSerializer(read_only=True)


    def create(self, validated_data):

        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        user_profile = UserProfile.objects.create(user=user, **validated_data)
        return user_profile

    def update(self, instance, validated_data):

        # Zaktualizuj tylko dane profilu
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Zapisz zaktualizowany profil
        instance.save()
        return instance