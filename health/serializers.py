from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile, Disease


class UserSerializer(serializers.ModelSerializer):
    """
    Serializator modelu użytkownika.
    
    Serializator obsługuje dane użytkownika, w tym nazwę użytkownika i adres e-mail. 
    Pole hasła jest tylko do zapisu, aby zapewnić bezpieczeństwo.
    """

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}


    def create(self, validated_data):
        """
        Tworzy i zwraca nową instancję użytkownika z zaszyfrowanym hasłem.
        
        Argumenty:
            validated_data (dict): Zweryfikowane dane zawierające szczegóły użytkownika.
        
        Zwraca:
            User: Nowo utworzona instancja użytkownika.
        """
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializator modelu profilu użytkownika.

    Serializator obsługuje dane użytkownika i jego profil, w tym dane osobowe oraz powiązane informacje o chorobie.
    Pole 'user' jest zagnieżdżonym serializatorem, który pozwala na przesyłanie pełnych danych użytkownika.
    Pole 'disease' pozwala na przypisanie choroby z istniejących rekordów w bazie danych.
    """
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
        """
        Inicjalizuje serializator i konfiguruje pole 'user' jako tylko do odczytu, 
        jeśli instancja jest dostępna (czyli przy aktualizacji profilu).

        Args:
            *args: Argumenty pozycyjne przekazywane do konstruktorów nadrzędnych.
            **kwargs: Argumenty nazwane przekazywane do konstruktorów nadrzędnych.
        """
        super().__init__(*args,**kwargs)

        if self.instance:
            self.fields["user"] = UserSerializer(read_only=True)


    def create(self, validated_data):
        """
        Tworzy i zwraca nową instancję profilu użytkownika, tworząc również nowego użytkownika 
        z danymi przesłanymi w żądaniu.

        Argumenty:
            validated_data (dict): Zweryfikowane dane zawierające szczegóły użytkownika oraz profil użytkownika.

        Zwraca:
            UserProfile: Nowo utworzona instancja profilu użytkownika.
        """
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        user_profile = UserProfile.objects.create(user=user, **validated_data)
        return user_profile

    def update(self, instance, validated_data):
        """
        Aktualizuje istniejący profil użytkownika z nowymi danymi, zachowując powiązanego użytkownika.

        Argumenty:
            instance (UserProfile): Istniejąca instancja profilu użytkownika, która ma zostać zaktualizowana.
            validated_data (dict): Zweryfikowane dane zawierające szczegóły użytkownika oraz profil użytkownika.

        Zwraca:
            UserProfile: Zaktualizowana instancja profilu użytkownika.
        """
       #Aktulizacja tylko danych w profilu
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance