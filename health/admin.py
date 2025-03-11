from django.contrib import admin
from .models import Symptom, Disease, UserSymptoms, DiseaseAdmin

admin.site.register(Symptom)
admin.site.register(Disease, DiseaseAdmin)
admin.site.register(UserSymptoms)
