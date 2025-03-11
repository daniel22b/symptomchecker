import os
import django
import sys
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Konfiguracja Django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "symptomchecker.settings")
django.setup()

# Import modeli
from health.models import Symptom, Disease

# Pobranie danych z bazy
def get_training_data():
    diseases = Disease.objects.all()
    symptoms = Symptom.objects.all()

    symptom_list = list(symptoms)
    symptom_map = {symptom.id: i for i, symptom in enumerate(symptom_list)}

    X = []
    y = []

    for disease in diseases:
        row = [0] * len(symptom_list)
        for symptom in disease.symptoms.all():
            row[symptom_map[symptom.id]] = 1
        X.append(row)
        y.append(disease.name)

    return np.array(X), np.array(y), symptom_map

# Pobierz dane
X, y, symptom_map = get_training_data()

# Podział na zbiór treningowy i testowy (80% trening, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Trenowanie modelu KNN
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

# Predykcja na zbiorze testowym
y_pred = knn.predict(X_test)

# Obliczenie dokładności
accuracy = accuracy_score(y_test, y_pred)
print(f"🎯 Dokładność modelu KNN: {accuracy:.2f}")

# Pełny raport klasyfikacji (precision, recall, F1-score)
print("\n📊 Raport klasyfikacji:")
print(classification_report(y_test, y_pred))
print(f"Zbiór treningowy: {X_train.shape}")
print(f"Zbiór testowy: {X_test.shape}")
from collections import Counter
print(Counter(y))  # Liczba przypadków każdej choroby
