from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = "core/index.html"

class LegalMentionsView(TemplateView):
    template_name = "core/legal_mentions.html"

class ContactUsView(TemplateView):
    template_name = "core/contact_us.html"
