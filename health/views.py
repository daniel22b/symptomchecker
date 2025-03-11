import numpy as np
from sklearn.neighbors import NearestNeighbors
from django.shortcuts import render, redirect
from .models import Disease, Symptom, UserSymptoms
from .forms import SymptomSelectionForm

def recommend_disease(request):
    if request.method == 'POST':
        form = SymptomSelectionForm(request.POST)
        if form.is_valid():
            # Pobranie zaznaczonych objawów
            selected_symptoms = form.cleaned_data['symptoms']
            
            # Tworzymy wektor binarny dla objawów użytkownika
            user_symptom_vector = np.array([1 if symptom in selected_symptoms else 0 for symptom in Symptom.objects.all()])
            
            # Przechodzimy przez wszystkie choroby i tworzymy wektory objawów
            disease_vectors = []
            disease_names = []
            for disease in Disease.objects.all():
                disease_vector = np.array([1 if symptom in disease.symptoms.all() else 0 for symptom in Symptom.objects.all()])
                disease_vectors.append(disease_vector)
                disease_names.append(disease.name)

            # Używamy KNN do porównania wektora objawów użytkownika z wektorami chorób
            model = NearestNeighbors(n_neighbors=1, metric='hamming')  # hamming dla porównania binarnych wektorów
            model.fit(disease_vectors)

            distances, indices = model.kneighbors([user_symptom_vector])

            # Pobieramy najbliższą chorobę
            recommended_disease = disease_names[indices[0][0]]
            return render(request, 'recommendation.html', {'recommended_disease': recommended_disease})
    else:
        form = SymptomSelectionForm()

    return render(request, 'select_symptoms.html', {'form': form})


def symptom_selection(request):
    if request.method == 'POST':
        form = SymptomSelectionForm(request.POST)
        if form.is_valid():
            return redirect('recommend_disease')
    else:
        form = SymptomSelectionForm()

    return render(request, 'select_symptoms.html', {'form': form})