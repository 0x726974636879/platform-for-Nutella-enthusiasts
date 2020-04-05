import random

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.views.generic import TemplateView

from .constants import HELLO_IN_DIFFERENT_LANGUAGES
from .forms import SignUpForm
from .viewmixins import LoginRequiredViewMixin


class HomePageView(LoginRequiredViewMixin, TemplateView):
    template_name = "core/index.html"

class LoginPageView(TemplateView):
    extra_context = {
        'focus': 'login'
    }
    template_name = "core/login_register.html"

    def post(self, request, **kwargs):
        """
        Override post method to authenticate a user.
        """
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user is not None and user.check_password(password) and user.is_active:
            user = authenticate(username=user.username, password=password)
            login(request, user)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

        return render(request, self.template_name)

class LogoutView(TemplateView):
    extra_context = {
        'focus': 'login'
    }
    template_name = "core/login_register.html"

    def get(self, request, **kwargs):
        """
        Override get method to logout the user.
        """
        logout(request)
        return render(request, self.template_name)

class SignUpView(TemplateView):
    extra_context = {
        'focus': 'signup'
    }
    template_name = "core/login_register.html"

    def post(self, request, **kwargs):
        """
        Override post method to create a user.
        """
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1')
            )
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})

class LegalMentionsView(LoginRequiredViewMixin, TemplateView):
    template_name = "core/legal_mentions.html"

class ContactUsView(LoginRequiredViewMixin, TemplateView):
    template_name = "core/contact_us.html"
