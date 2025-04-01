# import random
# import django
# import os

# # Inicjalizujemy Django (potrzebne do uruchomienia poza shell)
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'symptomchecker.settings')
# django.setup()

# # Importujemy modele
# from django.contrib.auth.models import User
# from health.models import UserProfile, Disease

# all_diseases = Disease.objects.all()

# for i in range(11,100 ):
#     username = f"user{i}"
#     email = f"user{i}@example.com"
#     password = "test1234"

#     user, created = User.objects.get_or_create(username=username, email=email)

#     if created:
#         user.set_password(password)
#         user.save()

#         random_disease = random.choice(all_diseases)

#         profile = UserProfile.objects.create(
#             user=user,  
#             first_name=f"Imię{i}",
#             last_name=f"Nazwisko{i}",
#             gender="M" if i % 2 == 0 else "K",
#             street=f"Ulica {i}",
#             city="Warszawa",
#             postal_code="00-000",
#             phone_number=f"12345678{i}",
#             disease=random_disease  
#         )

#         print(f"Utworzono użytkownika: {username} z profilem i losową chorobą: {random_disease.name}")
#     else:
#         print(f"Użytkownik {username} już istnieje!")
# import django
# from health.models import UserProfile
# import random

# profiles = UserProfile.objects.all()

# for profile in profiles:
#     profile.age = random.randint(10, 60)  # Losowy wiek od 10 do 60
#     profile.save()
