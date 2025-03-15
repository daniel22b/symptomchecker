import numpy as np
from sklearn.neighbors import NearestNeighbors
from django.shortcuts import render, redirect
from .models import Disease, Symptom, UserSymptoms
from .forms import SymptomSelectionForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.contrib import messages

@login_required
def recommend_disease(request):
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

            # Pobieramy najbliższą chorobę
            recommended_disease = disease_instances[indices[0][0]]

            user_profile.disease = recommended_disease
            user_profile.save()

            return render(request, 'recommendation.html', {'recommended_disease': recommended_disease})
    else:
        form = SymptomSelectionForm()

    return render(request, 'select_symptoms.html', {'form': form})

@login_required
def symptom_selection(request):
    if request.method == 'POST':
        form = SymptomSelectionForm(request.POST)
        if form.is_valid():
            return redirect('recommend_disease')
    else:
        form = SymptomSelectionForm()

    return render(request, 'select_symptoms.html', {'form': form})


def register(request):
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

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # return redirect("select_symptom")
            return redirect("welcome")
        else:
            messages.error(request, "Nie ma takiego konta.")
    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("login")


def home(request):
    return render(request, "home.html")  


#----------------------------------------------------
from django.shortcuts import render, redirect
from .forms import UserProfileForm

def complete_profile(request):
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


from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def welcome(request):
    return render(request, "welcome.html", {"username": request.user.username})
