from django.db import models
from django.contrib.auth.models import User

# Model objawu, np. ból głowy, kaszel itp.
class Symptom(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Model choroby, która jest związana z objawami
class Disease(models.Model):
    name = models.CharField(max_length=100)
    symptoms = models.ManyToManyField(Symptom)

    def __str__(self):
        return self.name

# Model użytkownika i jego objawów
class UserSymptoms(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symptoms = models.ManyToManyField(Symptom)

    def __str__(self):
        return f"Objawy użytkownika {self.user.username}"

from django.contrib import admin
from .models import Symptom, Disease, UserSymptoms

# Klasa konfiguracji admina dla modelu Disease
class DiseaseAdmin(admin.ModelAdmin):
    # filter_horizontal powoduje, że pole ManyToMany (symptoms) będzie wyświetlane w formie listy z przyciskami
    filter_horizontal = ('symptoms',)  # Umożliwia łatwiejsze wybieranie wielu objawów
