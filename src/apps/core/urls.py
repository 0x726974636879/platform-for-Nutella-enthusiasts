from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('legal_mentions/', views.LegalMentionsView.as_view(), name='legal_mentions'),
    path('contact_us/', views.ContactUsView.as_view(), name='contact'),
]