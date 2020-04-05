from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View


class LoginRequiredViewMixin(LoginRequiredMixin, View):
    extra_context = {
        'title': 'login'
    }
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
