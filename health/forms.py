from django import forms
from .models import Symptom, UserProfile
from django.contrib.auth.models import User

class SymptomSelectionForm(forms.Form):
    """
    Formularz służący do wyboru objawów.

    Umożliwia użytkownikowi wybór wielu objawów za pomocą pól wyboru (checkbox).
    Pole jest wymagane (required), a dane są pobierane z modelu `Symptom`.
    """
    symptoms = forms.ModelMultipleChoiceField(
        queryset=Symptom.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )


class RegisterForm(forms.ModelForm):
    """
    Formularz rejestracji użytkownika.

    Formularz do rejestracji nowego użytkownika, ustawia nazwy użytkownika,
    adresu e-mail oraz hasła. Hasło jest wymagane, a pole 'password_confirm' pozwala na 
    weryfikację poprawności wpisanych haseł.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(max_length=12, help_text='')
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        """
        Sprawdza, czy hasła są identyczne.

        Jeśli hasła wprowadzone w polach 'password' i 'password_confirm' nie są zgodne,
        zostanie zgłoszony błąd walidacji. Formularz nie przejdzie walidacji, dopóki hasła
        nie będą takie same.

        Zwraca:
            cleaned_data (dict): Zweryfikowane dane formularza, jeśli walidacja zakończyła się sukcesem.
        
        Zgłasza:
            forms.ValidationError: Jeśli hasła nie są identyczne.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Hasła muszą być identyczne.")

        return cleaned_data

class UserProfileForm(forms.ModelForm):
    """
    Formularz edycji profilu użytkownika.

    Formularz umożliwia użytkownikowi edycję swojego profilu, w tym imienia, nazwiska,
    płci, adresu zamieszkania i innych danych kontaktowych. Formularz jest powiązany z modelem
    `UserProfile` i pozwala na wprowadzenie takich danych jak: imię, nazwisko, miasto, numer telefonu itp.
    """

    class Meta:
        model = UserProfile
        fields = ["first_name", "last_name", "gender", "street",
                   "city",
                 "postal_code", "phone_number","age",]


