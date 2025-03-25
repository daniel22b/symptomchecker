from django import forms
from .models import Symptom, UserProfile
from django.contrib.auth.models import User

class SymptomSelectionForm(forms.Form):
    symptoms = forms.ModelMultipleChoiceField(
        queryset=Symptom.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(max_length=12, help_text='')
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Hasła muszą być identyczne.")

        return cleaned_data

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ["first_name", "last_name", "gender", "street",
                   "city",
                 "postal_code", "phone_number","age",]


