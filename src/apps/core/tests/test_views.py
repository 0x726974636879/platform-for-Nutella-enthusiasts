from django.contrib.auth.models import User
from django.http.response import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse

from friendship.models import Friend, FriendshipRequest

from apps.core.views import (
    AcceptFriendShip,
    AddFriend,
    CancelFriendRequest,
    FriendProductsSaved,
    RejectFriendShip,
    RemoveFriendShip,
    SearchFriend,
)
from apps.resources.models import BackupProduct, Product
from apps.resources.tests.utils import create_products


home = reverse("core:home")
legal_mentions = reverse("core:legal_mentions")
login = reverse("core:login")
logout = reverse("core:logout")
profil = reverse("core:profil")
friendship = reverse("core:friendship")


credentials = [
    {
        "username": "testuser1",
        "email": "testuser1@free.fr",
        "password": "1X<ISRUkw+tuK"
    },
    {
        "username": "testuser2",
        "email": "testuser2@free.fr",
        "password": "adadfgfdsgfd"
    }
]


class HomePageViewTest(TestCase):
    def test_view_url_exists(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(home)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(home)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")


class LogoutViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(**credentials[0])
        test_user1.save()

    def test_can_logout(self):
        # Connection.
        response = self.client.post(
            "/login/",
            {
                "email": credentials[0]["email"],
                "password": credentials[0]["password"]
            }
        )
        # Try to go to the profil page.
        response = self.client.get(profil)
        self.assertEqual(response.status_code, 200)
        # Disconnect.
        response = self.client.get(logout)
        self.assertEqual(response.status_code, 302)


class LoginPageViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(**credentials[0])
        test_user1.save()

    def test_view_url_exists(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(login)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(login)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/login.html")

    def test_redirect_to_home_if_logged_in(self):
        _ = self.client.post(
            "/login/",
            {
                "email": credentials[0]["email"],
                "password": credentials[0]["password"]
            }
        )
        response = self.client.get(login)
        self.assertEqual(response.status_code, 302)

    def test_redirect_connection_refused(self):
        login = self.client.login(
            email=credentials[0]["email"], password="1234"
        )
        self.assertFalse(login)


class ProfilViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(**credentials[0])
        test_user1.save()

    def test_view_url_exists(self):
        _ = self.client.login(**credentials[0])
        response = self.client.get("/profil/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        _ = self.client.login(**credentials[0])
        response = self.client.get(profil)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        _ = self.client.login(**credentials[0])
        response = self.client.get(profil)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/profil.html")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(profil)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/login"))


class LegalMentionsViewTest(TestCase):
    def test_view_url_exists(self):
        response = self.client.get("/legal_mentions", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(legal_mentions)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(legal_mentions)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/legal_mentions.html")


class FriendShipViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(**credentials[0])
        test_user1.save()

    def test_view_url_exists(self):
        response = self.client.get("/friends", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.post(
            "/login/",
            {
                "email": credentials[0]["email"],
                "password": credentials[0]["password"]
            }
        )
        response = self.client.get(friendship)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.post(
            "/login/",
            {
                "email": credentials[0]["email"],
                "password": credentials[0]["password"]
            }
        )
        response = self.client.get(friendship)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/friendship.html")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(friendship)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/login"))

    def test_context_data(self):
        self.client.post(
            "/login/",
            {
                "email": credentials[0]["email"],
                "password": credentials[0]["password"]
            }
        )
        response = self.client.get("/friends", follow=True)
        self.assertIn("friendship", response.context_data.keys())
        self.assertIn("friends", response.context_data.keys())
        self.assertIn("friendship_request_sent", response.context_data.keys())


class AcceptFriendShipTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(**credentials[0])
        self.test_user2 = User.objects.create_user(**credentials[1])
        Friend.objects.add_friend(self.test_user1, self.test_user2)
        self.factory = RequestFactory()

    def test_view_url_exists(self):
        request = self.factory.get(
            "/friends/{self.test_user1}/accept", follow=True
        )
        request.user = self.test_user2
        response = AcceptFriendShip.as_view()(request, id=self.test_user1.id)
        self.assertTrue(response.url.startswith("/friends"))

    def test_view_url_accessible_by_name(self):
        request = self.factory.get(
            reverse("core:accept_friend", kwargs={"id": self.test_user1.id}),
            follow=True
        )
        request.user = self.test_user2
        response = AcceptFriendShip.as_view()(request, id=self.test_user1.id)
        self.assertTrue(response.url.startswith("/friends"))

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            f"/friends/{self.test_user1.id}/accept"
        )
        self.assertTrue(response.url.startswith("/login"))

    def test_friendship_accepted(self):
        request = self.factory.get(
            "/friends/{self.test_user1}/accept", follow=True
        )
        request.user = self.test_user2
        AcceptFriendShip.as_view()(request, id=self.test_user1.id)
        self.assertEqual(
            Friend.objects.filter(from_user=self.test_user1).count(), 1
        )


class RejectFriendShipTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(**credentials[0])
        self.test_user2 = User.objects.create_user(**credentials[1])
        Friend.objects.add_friend(self.test_user1, self.test_user2)
        self.factory = RequestFactory()

    def test_view_url_exists(self):
        request = self.factory.get(
            "/friends/{self.test_user1.id}/reject", follow=True
        )
        request.user = self.test_user2
        response = RejectFriendShip.as_view()(
            request, id=self.test_user1.id
        )
        self.assertTrue(response.url.startswith("/friends"))

    def test_view_url_accessible_by_name(self):
        request = self.factory.get(
            reverse("core:reject_friend", kwargs={"id": self.test_user1.id}),
            follow=True
        )
        request.user = self.test_user2
        response = RejectFriendShip.as_view()(
            request, id=self.test_user1.id
        )
        self.assertTrue(response.url.startswith("/friends"))

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            f"/friends/{self.test_user1.id}/reject"
        )
        self.assertTrue(response.url.startswith("/login"))

    def test_friendship_rejected(self):
        request = self.factory.get(
            "/friends/{self.test_user1.id}/reject", follow=True
        )
        request.user = self.test_user2
        RejectFriendShip.as_view()(request, id=self.test_user1.id)
        self.assertEqual(
            Friend.objects.filter(to_user=self.test_user1).count(), 0
        )


class RemoveFriendShipTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(**credentials[0])
        self.test_user2 = User.objects.create_user(**credentials[1])
        self.friendship = Friend.objects.add_friend(
            self.test_user1, self.test_user2
        )
        self.factory = RequestFactory()

    def test_view_url_exists(self):
        request = self.factory.get(
            "/friends/{self.test_user1.id}/remove", follow=True
        )
        request.user = self.test_user2
        response = RemoveFriendShip.as_view()(
            request, id=self.test_user1.id
        )
        self.assertTrue(response.url.startswith("/friends"))

    def test_view_url_accessible_by_name(self):
        request = self.factory.get(
            reverse("core:remove_friend", kwargs={"id": self.test_user1.id}),
            follow=True
        )
        request.user = self.test_user2
        response = RemoveFriendShip.as_view()(
            request, id=self.test_user1.id
        )
        self.assertTrue(response.url.startswith("/friends"))

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            f"/friends/{self.test_user1.id}/remove"
        )
        self.assertTrue(response.url.startswith("/login"))

    def test_friendship_removed(self):
        FriendshipRequest.objects.get(from_user=self.test_user1).accept()
        request = self.factory.get(
            "/friends/{self.test_user1.id}/remove", follow=True
        )
        request.user = self.test_user2
        RemoveFriendShip.as_view()(request, id=self.test_user2.id)
        self.assertEqual(
            FriendshipRequest.objects.filter(
                from_user=self.test_user1
            ).count(),
            0
        )


class CancelFriendRequestTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(**credentials[0])
        self.test_user2 = User.objects.create_user(**credentials[1])
        Friend.objects.add_friend(self.test_user1, self.test_user2)
        self.friendship = FriendshipRequest.objects.get(
            from_user=self.test_user1
        )
        self.factory = RequestFactory()

    def test_view_url_exists(self):
        request = self.factory.get(
            "/friends/{self.friendship.id}/cancel_friend_request", follow=True
        )
        request.user = self.test_user1
        response = CancelFriendRequest.as_view()(
            request, id=self.friendship.id
        )
        self.assertTrue(response.url.startswith("/friends"))

    def test_view_url_accessible_by_name(self):
        request = self.factory.get(
            reverse(
                "core:cancel_friend_request", kwargs={"id": self.friendship.id}
            ),
            follow=True
        )
        request.user = self.test_user1
        response = CancelFriendRequest.as_view()(
            request, id=self.friendship.id
        )
        self.assertTrue(response.url.startswith("/friends"))

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            f"/friends/{self.friendship.id}/cancel_friend_request"
        )
        self.assertTrue(response.url.startswith("/login"))

    def test_friendship_canceled(self):
        self.assertEqual(
            FriendshipRequest.objects.filter(
                from_user=self.test_user1
            ).count(),
            1
        )
        request = self.factory.get(
            "/friends/{self.friendship.id}/cancel_friend_request", follow=True
        )
        request.user = self.test_user1
        CancelFriendRequest.as_view()(request, id=self.friendship.id)
        self.assertEqual(
            FriendshipRequest.objects.filter(
                from_user=self.test_user1
            ).count(),
            0
        )


class SearchFriendTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(**credentials[0])
        self.test_user2 = User.objects.create_user(**credentials[1])
        self.factory = RequestFactory()

    def test_view_url_exists(self):
        request = self.factory.post(
            "/search_friend",
            {"username": self.test_user2.username}
        )
        request.user = self.test_user1
        response = SearchFriend.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        request = self.factory.post(
            reverse("core:search_friend"),
            {"username": self.test_user2.username}
        )
        request.user = self.test_user1
        response = SearchFriend.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.post(
            reverse("core:search_friend"),
            {"username": self.test_user2.username}
        )
        self.assertTrue(response.url.startswith("/login"))

    def test_friend_founded(self):
        request = self.factory.post(
            reverse("core:search_friend"),
            {"username": self.test_user2.username}
        )
        request.user = self.test_user1
        response = SearchFriend.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_friend_not_founded(self):
        request = self.factory.post(
            reverse("core:search_friend"),
            {"username": "unknown"}
        )
        request.user = self.test_user1
        response = SearchFriend.as_view()(request)
        self.assertEqual(response.status_code, 404)


class AddFriendTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(**credentials[0])
        self.test_user2 = User.objects.create_user(**credentials[1])
        self.data = {"user_id": self.test_user2.id}
        self.factory = RequestFactory()

    def test_view_url_exists(self):
        request = self.factory.post("/add_friend", self.data)
        request.user = self.test_user1
        response = AddFriend.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        request = self.factory.post(reverse("core:add_friend"), self.data)
        request.user = self.test_user1
        response = SearchFriend.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.post(reverse("core:add_friend"), self.data)
        self.assertTrue(response.url.startswith("/login"))

    def test_friend_not_found(self):
        self.data["username"] = "unknown"
        request = self.factory.post(reverse("core:add_friend"), self.data)
        request.user = self.test_user1
        response = SearchFriend.as_view()(request)
        self.assertEqual(response.status_code, 404)

    def test_friend_added(self):
        request = self.factory.post(reverse("core:add_friend"), self.data)
        request.user = self.test_user1
        response = SearchFriend.as_view()(request)
        self.assertEqual(response.status_code, 200)


class FriendProductsSavedTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(**credentials[0])
        self.test_user2 = User.objects.create_user(**credentials[1])
        Friend.objects.add_friend(self.test_user1, self.test_user2)
        create_products(10)
        # Create product saved by the user.
        for product in Product.objects.all()[:5]:
            BackupProduct.objects.create(
                product_code=product.code,
                category_name=product.category.name,
                user=self.test_user2
            )
        self.factory = RequestFactory()

    def test_view_url_exists(self):
        FriendshipRequest.objects.get(from_user=self.test_user1).accept()
        request = self.factory.get(
            f"/friends/{self.test_user2.id}/products_saved", follow=True
        )
        request.user = self.test_user1
        response = FriendProductsSaved.as_view()(
            request, id=self.test_user2.id
        )
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        FriendshipRequest.objects.get(from_user=self.test_user1).accept()
        request = self.factory.get(
            reverse(
                "core:friend_products_saved", kwargs={"id": self.test_user2.id}
            ),
            follow=True
        )
        request.user = self.test_user1
        response = FriendProductsSaved.as_view()(
            request, id=self.test_user2.id
        )
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        FriendshipRequest.objects.get(from_user=self.test_user1).accept()
        response = self.client.get(
            reverse(
                "core:friend_products_saved", kwargs={"id": self.test_user2.id}
            )
        )
        self.assertTrue(response.url.startswith("/login"))

    def test_friendship_not_found(self):
        request = self.factory.get(
            reverse(
                "core:friend_products_saved", kwargs={"id": self.test_user2.id}
            ),
        )
        request.user = self.test_user1
        response = FriendProductsSaved.as_view()(
            request, id=self.test_user2.id
        )
        self.assertEqual(response.status_code, 404)

    def test_user_not_found(self):
        request = self.factory.get(
            reverse(
                "core:friend_products_saved", kwargs={"id": 30}
            ),
        )
        request.user = self.test_user1
        with self.assertRaises(Http404):
            FriendProductsSaved.as_view()(request, id=30)

    def test_context(self):
        FriendshipRequest.objects.get(from_user=self.test_user1).accept()
        self.client.post(
            "/login/",
            {
                "email": credentials[0]["email"],
                "password": credentials[0]["password"]
            }
        )
        response = self.client.get(
            f"/friends/{self.test_user2.id}/products_saved"
        )
        self.assertIn("friend", response.context_data.keys())
        self.assertIn("products", response.context_data["friend"].keys())
        self.assertEqual(len(response.context_data["friend"]["products"]), 5)
