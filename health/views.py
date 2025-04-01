import numpy as np
from sklearn.neighbors import NearestNeighbors
from .models import Disease, Symptom, UserProfile
from .forms import SymptomSelectionForm, UserProfileForm, RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, generics
from django.contrib.auth.models import User
from .serializers import UserSerializer,UserProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse


class UserView(viewsets.ModelViewSet):
    """Widok API dla użytkowników."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileView(viewsets.ModelViewSet):
    """Widok API dla profili użytkowników."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

@login_required
def recommend_disease(request):
    """Przewidywana choroba na podstawie wybranych objawów użytkownika."""
    user_profile = request.user.userprofile 
    if request.method == 'POST':
        form = SymptomSelectionForm(request.POST)
        if form.is_valid():
            # Pobranie zaznaczonych objawów
            selected_symptoms = form.cleaned_data['symptoms']
            
            if not selected_symptoms.exists():  # Jeśli użytkownik nie wybrał objawów
                return render(request, 'recommendation.html', {'error': 'Nie wybrano żadnych objawów!'})

            symptom_list = list(Symptom.objects.all())
            user_symptom_vector = np.array([1 if symptom in selected_symptoms else 0 for symptom in symptom_list])

            # choroby i  wektory objawów
            disease_vectors = []
            disease_instances = list(Disease.objects.all())

            if not disease_instances:
                return render(request, 'recommendation.html', {'error': 'Brak danych o chorobach!'})
            
            for disease in Disease.objects.all():
                disease_vector = np.array([1 if symptom in disease.symptoms.all() else 0 for symptom in symptom_list])
                disease_vectors.append(disease_vector)

            # KNN do porównania wektora objawów użytkownika z wektorami chorób
            model = NearestNeighbors(n_neighbors=1, metric='hamming')  # hamming dla porównania binarnych wektorów
            model.fit(disease_vectors)

            distances, indices = model.kneighbors([user_symptom_vector])

            # Najbliższs choroba
            recommended_disease = disease_instances[indices[0][0]]

            user_profile.disease = recommended_disease
            user_profile.save()

            return render(request, 'recommendation.html', {'recommended_disease': recommended_disease})
    else:
        form = SymptomSelectionForm()

    return render(request, 'select_symptoms.html', {'form': form})

@login_required
def symptom_selection(request):
    """Widok umożliwiający użytkownikowi wybór objawów."""
    if request.method == 'POST':
        form = SymptomSelectionForm(request.POST)
        if form.is_valid():
            return redirect('recommend_disease')
    else:
        form = SymptomSelectionForm()

    return render(request, 'select_symptoms.html', {'form': form})

@login_required
def welcome(request):
    """Ekran powitalny dla zalogowanego użytkownika."""
    return render(request, "welcome.html", {"username": request.user.username})


def user_login(request):
    """Logowanie użytkownika."""

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("welcome")
        else:
            messages.error(request, "Nie ma takiego konta.")
    return render(request, "login.html")



def user_logout(request):
    """Wylogowanie użytkownika."""
    logout(request)
    return redirect("login")


def register(request):
    """Rejestracja nowego użytkownika."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("complete_profile")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def complete_profile(request):
    """Uzupełnianie profilu użytkownika po rejestracji."""
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect("welcome")  # Przekierowanie po uzupełnieniu danych
    else:
        form = UserProfileForm()
    
    return render(request, "complete_profile.html", {"form": form})

def home(request):
    """Strona główna aplikacji."""
    return render(request, "home.html")  


#FAZA TESTOWA
# def generate_chart(request):
    user_profile = UserProfile.objects.all()

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    values = [10, 15, 7, 20, 5] 

    chart_type = request.GET.get('chart_type', 'pie') 

    fig, ax = plt.subplots()
    if chart_type == 'bar':
        ax.bar(months, values)
    elif chart_type == 'line':
        ax.plot(months, values)
    elif chart_type == 'pie':
        ax.pie(values, labels=months, autopct='%1.1f%%')

   
    ax.set_title('Liczba transakcji w różnych miesiącach')
    ax.set_xlabel('')
    ax.set_ylabel('Liczba transakcji')
    
 
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return HttpResponse(buf, content_type='image/png')


# import random
# profiles = UserProfile.objects.all()

# for profile in profiles:
#     profile.age = random.randint(10, 60)  
#     profile.save()