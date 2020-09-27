from friendship.models import Friend, FriendshipRequest

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import (
    get_object_or_404,
    HttpResponseRedirect,
    render,
    redirect
)
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from django.urls import reverse

from .forms import LoginForm, SignUpForm, SearchUserForm
from .utils import get_friendship


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

    def dispatch(self, request, *args, **kwargs):
        """
        Override dispatch method to redirect user if a user attempts to
        get the login page when the user is already logged.
        """
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("core:home"))
        return super().dispatch(request, *args, **kwargs)

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


class ProfilView(LoginRequiredMixin, TemplateView):
    """
    Profil page view.
    """
    template_name = "core/profil.html"


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


class FriendShip(LoginRequiredMixin, FormView):
    """
    Friendship page view.
    """
    form_class = SearchUserForm
    template_name = "core/friendship.html"

    def get(self, request, *args, **kwargs):
        """
        Get all the friendship requests.
        """
        kwargs.update(get_friendship(request.user))
        return self.render_to_response(self.get_context_data(**kwargs))


class AcceptFriendShip(LoginRequiredMixin, View):
    template_name = "core/friendship.html"

    def get(self, request, *args, **kwargs):
        """
        Override get method to accept a friend.
        """
        other_user = get_object_or_404(User, pk=kwargs["id"])
        friend_request = FriendshipRequest.objects.get(
            from_user=other_user, to_user=request.user
        )
        friend_request.accept()
        return HttpResponseRedirect(reverse("core:friendship"))


class RejectFriendShip(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """
        Override get method to reject a friend.
        """
        other_user = get_object_or_404(User, pk=kwargs["id"])
        friend_request = FriendshipRequest.objects.get(
            from_user=other_user, to_user=request.user
        )
        friend_request.delete()
        return HttpResponseRedirect(reverse("core:friendship"))


class RemoveFriendShip(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """
        Override get method to delete a friendship between two
        users.
        """
        other_user = get_object_or_404(User, pk=kwargs["id"])
        Friend.objects.remove_friend(self.request.user, other_user)
        return HttpResponseRedirect(reverse("core:friendship"))


class CancelFriendRequest(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """
        Override get method to cancel a friendship sent.
        """
        try:
            FriendshipRequest.objects.get(id=kwargs["id"]).delete()
        except FriendshipRequest.DoesNotExist:
            pass
        finally:
            return HttpResponseRedirect(reverse("core:friendship"))


class SearchFriend(LoginRequiredMixin, FormView):
    template_name = "core/friendship.html"
    form_class = SearchUserForm

    def post(self, request, **kwargs):
        """
        Override post method to search a user.
        """
        form = SearchUserForm(data=request.POST)
        kwargs.update(get_friendship(request.user))
        context = {
            "form": form,
            **kwargs
        }
        if form.is_valid():
            # Retrieve email and password informations.
            username = form.cleaned_data.get("username")
            if username != self.request.user.username:
                # Get the user.
                try:
                    user = User.objects.get(username=username)
                    context["user_found"] = user
                except User.DoesNotExist:
                    error_msg = f"L'utilisateur {username} n'existe pas"
                    form.add_error("username", error_msg)
                    return render(request, self.template_name, context)
                return render(request, self.template_name, context)
        return render(request, self.template_name, context)


class AddFriend(LoginRequiredMixin, View):
    template_name = "core/friendship.html"

    def post(self, request, **kwargs):
        """
        Override post method to add a friend.
        """
        other_user = get_object_or_404(User, pk=request.POST["user_id"])
        Friend.objects.add_friend(
            request.user,
            other_user,
            message="Hey tu veux devenir mon ami ? :-)"
        )
        kwargs.update(get_friendship(request.user))
        context = {
            "form": SearchUserForm(),
            **kwargs
        }
        return render(request, self.template_name, context)
