from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Prenom.'
    )
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Nom.'
    )
    email = forms.EmailField(
        max_length=254, help_text='Entrez une adresse email valide.'
    )

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password1',
            'password2'
        )


class ProductSearchForm(forms.Form):
    product_name = forms.CharField(
        help_text='Nom du produit.',
        label="Nom du produit",
        max_length=100,
        min_length=2,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Chercher'
            }
        )
    )
