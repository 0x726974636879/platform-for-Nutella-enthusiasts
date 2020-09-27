from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(
        help_text="Entrez une adresse email valide.",
        label="Adresse email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={"class": "form-control"}
        )
    )
    password = forms.CharField(
        help_text="Entrez votre mot de passe.",
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        help_text="Entrez votre pseudo.",
        label="Pseudo",
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    first_name = forms.CharField(
        help_text="Entrez votre prenom.",
        label="Prenom",
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    last_name = forms.CharField(
        help_text="Entrez votre nom.",
        label="Nom",
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    email = forms.EmailField(
        help_text="Entrez une adresse email valide.",
        label="Adresse email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={"class": "form-control"}
        )
    )
    password1 = forms.CharField(
        help_text="Entrez votre mot de passe.",
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        )
    )
    password2 = forms.CharField(
        help_text="Entrez le même mot de passe que ci-dessus, pour vérification.",
        label="Verification de mot de passe.",
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        )
    )

    class Meta:
        model = User
        fields = (
            "username", "first_name", "last_name", "email", "password1",
            "password2"
        )


class SearchUserForm(forms.Form):
    username = forms.CharField(
        label="Utilisateur",
        help_text="Rechercher un utilisateur",
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
