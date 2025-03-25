from django.contrib import admin
from .models import Symptom, Disease, DiseaseAdmin, UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'city', 'phone_number', 'disease')
    search_fields = ('user__username', 'first_name', 'last_name',"age")

admin.site.register(Symptom)
admin.site.register(Disease, DiseaseAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
