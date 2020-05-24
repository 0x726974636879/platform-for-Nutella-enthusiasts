from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import LoginForm, SignUpForm


class HomePageView(TemplateView):
    """
    Home page view.
    """
    template_name = "core/index.html"


class LoginPageView(FormView):
    """
    Login page view.
    """
    form_class = LoginForm
    template_name = "core/login.html"

    def post(self, request, **kwargs):
        """
        Override post method to authenticate a user.
        """
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # Retrieve email and password informations.
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            # Get the user.
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                error_msg = "L'adresse email renseignée n'est pas valide."
                form.add_error("email", error_msg)
                return render(request, self.template_name, {"form": form})
            # Try to connect with the user.
            is_correct_password = user.check_password(password)
            if user is not None and is_correct_password and user.is_active:
                user = authenticate(username=user.username, password=password)
                login(request, user)
                return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
            elif not is_correct_password:
                form.add_error("password", "Mot de passe incorrect.")
            return render(request, self.template_name, {"form": form})

        return render(request, self.template_name, {"form": form})


class LogoutView(TemplateView):
    """
    Logout page view.
    """

    def get(self, request, **kwargs):
        """
        Override get method to logout the user.
        """
        logout(request)
        return redirect("core:home")


class SignUpView(FormView):
    """
    Sign up page view.
    """
    form_class = SignUpForm
    template_name = "core/signup.html"

    def post(self, request, **kwargs):
        """
        Override post method to create a user.
        """
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password1")
            )
            login(request, user)
            return redirect("core:home")
        return render(request, self.template_name, {"form": form})


class LegalMentionsView(TemplateView):
    """
    Legal mentions page view.
    """
    template_name = "core/legal_mentions.html"
