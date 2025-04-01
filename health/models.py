from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class Symptom(models.Model):
    """
    Model reprezentujący objaw choroby, np. ból głowy, kaszel itp.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Disease(models.Model):
    """
    Model reprezentujący chorobę, która jest związana z określonymi objawami.
    """
    name = models.CharField(max_length=100)
    symptoms = models.ManyToManyField(Symptom)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name



class DiseaseAdmin(admin.ModelAdmin):
    """
    Konfiguracja modelu Disease w panelu administracyjnym Django.
    """
    filter_horizontal = ('symptoms',)  
    

class UserProfile(models.Model):
    """
    Model przechowujący dodatkowe informacje o użytkowniku, w tym dane osobowe oraz powiązaną chorobę.
    """
    GENDER_CHOICES = [
        ('M', 'Mężczyzna'),
        ('K', 'Kobieta'),
        ('I', 'Inne'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    street = models.CharField(max_length=25)
    city = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=6  )
    phone_number = models.CharField(max_length=9)
    age = models.IntegerField(null=True, blank=True)
    disease = models.ForeignKey('Disease', null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

