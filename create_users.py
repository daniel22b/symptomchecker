import random
import django
import os

# Inicjalizujemy Django (potrzebne do uruchomienia poza shell)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'symptomchecker.settings')
django.setup()

# Importujemy modele
from django.contrib.auth.models import User
from health.models import UserProfile, Disease

# Pobieramy wszystkie choroby z bazy danych
all_diseases = Disease.objects.all()

for i in range(11,100 ):
    # Tworzymy użytkownika
    username = f"user{i}"
    email = f"user{i}@example.com"
    password = "test1234"

    user, created = User.objects.get_or_create(username=username, email=email)

    if created:
        # Ustawiamy hasło
        user.set_password(password)
        user.save()

        # Losujemy chorobę z dostępnych chorób
        random_disease = random.choice(all_diseases)

        # Tworzymy profil użytkownika
        profile = UserProfile.objects.create(
            user=user,  # Powiązanie z użytkownikiem
            first_name=f"Imię{i}",
            last_name=f"Nazwisko{i}",
            gender="M" if i % 2 == 0 else "K",
            street=f"Ulica {i}",
            city="Warszawa",
            postal_code="00-000",
            phone_number=f"12345678{i}",
            disease=random_disease  # Losowa choroba przypisana do użytkownika
        )

        print(f"Utworzono użytkownika: {username} z profilem i losową chorobą: {random_disease.name}")
    else:
        print(f"Użytkownik {username} już istnieje!")
