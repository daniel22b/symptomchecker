from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Model objawu, np. ból głowy, kaszel itp.
class Symptom(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Model choroby, która jest związana z objawami
class Disease(models.Model):
    name = models.CharField(max_length=100)
    symptoms = models.ManyToManyField(Symptom)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Klasa konfiguracji admina dla modelu Disease
class DiseaseAdmin(admin.ModelAdmin):
    filter_horizontal = ('symptoms',)  
    

class UserProfile(models.Model):
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

