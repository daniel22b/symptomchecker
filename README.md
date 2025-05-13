#  SymptomChecker

**SymptomChecker** to aplikacja webowa stworzona w Django, która umożliwia użytkownikom wybór objawów oraz otrzymywanie rekomendacji potencjalnych chorób. Aplikacja wspiera również rejestrację, logowanie i edycję profilu użytkownika.

##  Funkcje

-  Rejestracja użytkownika z weryfikacją hasła
-  Logowanie i wylogowanie
-  Uzupełnianie profilu użytkownika (wiek, płeć, adres, telefon itd.)
-  Wybór objawów z listy checkboxów
-  Rekomendacja chorób na podstawie wybranych objawów
-  Panel administratora Django do zarządzania objawami, chorobami i profilami
-  API oparte na Django REST Framework (DRF)

## 🛠 Technologie

- Python 3.x
- Django
- Django REST Framework
- HTML/CSS (Django Templates)
- SQLite (domyślna baza danych)

##  Instalacja

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/daniel22b/symptomchecker.git
   cd symptomchecker
2. Utwórz środowisko wirtualne i je aktywuj:
  python -m venv venv
  source venv/bin/activate        # Linux/macOS
  venv\Scripts\activate           # Windows
3. Przeprowadź migrację
   python manage.py migrate
4. Uruchom serwer developerski:
   python manage.py runserver
5. Otwórz przeglądarkę i przejdź do:
   http://127.0.0.1:8000/

##  Struktura katalogów
symptomchecker/
├── health/

│   ├── models.py

│   ├── views.py

│   ├── forms.py

│   ├── serializers.py

│   ├── urls.py

├── templates/

│   └── health/

│       ├── register.html

│       ├── login.html

│       ├── select_symptoms.html

│       └── ...

├── static/

├── manage.py

└── README.md
