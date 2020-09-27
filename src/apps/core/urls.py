from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path(
        "legal_mentions/",
        views.LegalMentionsView.as_view(),
        name="legal_mentions"
    ),
    path("login/", views.LoginPageView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("profil/", views.ProfilView.as_view(), name="profil"),
    path("friends/", views.FriendShip.as_view(), name="friendship"),
    path(
        "search_friend/",
        views.SearchFriend.as_view(),
        name="search_friend"
    ),
    path(
        "add_friend/",
        views.AddFriend.as_view(),
        name="add_friend"
    ),
    path(
        "friends/<int:id>/remove",
        views.RemoveFriendShip.as_view(),
        name="remove_friend"
    ),
    path(
        "friends/<int:id>/accept",
        views.AcceptFriendShip.as_view(),
        name="accept_friend"
    ),
    path(
        "friends/<int:id>/reject",
        views.RejectFriendShip.as_view(),
        name="reject_friend"
    ),
    path(
        "friends/<int:id>/cancel_friend_request",
        views.CancelFriendRequest.as_view(),
        name="cancel_friend_request"
    )
]
