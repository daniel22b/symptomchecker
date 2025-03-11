
from django.contrib import admin
from django.urls import path
from health import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('select-symptoms/', views.symptom_selection, name='select_symptoms'),
    path('recommend-disease/', views.recommend_disease, name='recommend_disease'),
]
