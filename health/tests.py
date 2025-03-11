from django.test import TestCase

from django.test import TestCase
from health.models import Symptom, Disease
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

class DiseasePredictionTest(TestCase):
    def setUp(self):
        """Przygotowanie danych testowych"""
        # Tworzymy objawy
        self.fever = Symptom.objects.create(name="gorączka")
        self.cough = Symptom.objects.create(name="kaszel")
        self.headache = Symptom.objects.create(name="ból głowy")

        # Tworzymy choroby i przypisujemy objawy
        self.flu = Disease.objects.create(name="grypa")
        self.flu.symptoms.add(self.fever, self.cough)

        self.migraine = Disease.objects.create(name="migrena")
        self.migraine.symptoms.add(self.headache)

    def test_knn_prediction(self):
        """Testowanie algorytmu KNN dla objawów"""
        # Pobranie danych z bazy
        data = []
        for disease in Disease.objects.all():
            symptoms = [symptom.id for symptom in disease.symptoms.all()]
            data.append((disease.id, symptoms))

        # Tworzymy tabelę dla KNN
        df = pd.DataFrame(data, columns=['disease_id', 'symptoms'])
        df = df.explode('symptoms').pivot_table(index='disease_id', columns='symptoms', aggfunc=lambda x: 1, fill_value=0)

        # Tworzenie modelu KNN
        model = NearestNeighbors(n_neighbors=1, metric='cosine')
        model.fit(df)

        # Test - jakie choroby pasują do objawów kaszel + gorączka
        test_symptoms = [self.fever.id, self.cough.id]  
        test_vector = np.zeros(df.shape[1])
        for s_id in test_symptoms:
            if s_id in df.columns:
                test_vector[df.columns.get_loc(s_id)] = 1

        distances, indices = model.kneighbors([test_vector])
        recommended_disease = df.index[indices[0][0]]

        # Sprawdzamy, czy KNN dopasował grypę
        self.assertEqual(Disease.objects.get(id=recommended_disease).name, "grypa")
