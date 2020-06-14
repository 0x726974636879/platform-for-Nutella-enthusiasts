from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


home = reverse("core:home")
legal_mentions = reverse("core:legal_mentions")
login = reverse("core:login")
logout = reverse("core:logout")
profil = reverse("core:profil")

credentials = {
    "username": "testuser1",
    "email": "testuser1@free.fr",
    "password": "1X<ISRUkw+tuK"
}


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
        test_user1 = User.objects.create_user(**credentials)
        test_user1.save()

    def test_can_logout(self):
        # Connection.
        response = self.client.post(
            "/login/",
            {
                "email": credentials["email"],
                "password": credentials["password"]
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
        test_user1 = User.objects.create_user(**credentials)
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
                "email": credentials["email"],
                "password": credentials["password"]
            }
        )
        response = self.client.get(login)
        self.assertEqual(response.status_code, 302)

    def test_redirect_connection_refused(self):
        login = self.client.login(
            email=credentials["email"], password="1234"
        )
        self.assertFalse(login)


class ProfilViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(**credentials)
        test_user1.save()

    def test_view_url_exists(self):
        _ = self.client.login(**credentials)
        response = self.client.get("/profil/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        _ = self.client.login(**credentials)
        response = self.client.get(profil)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        _ = self.client.login(**credentials)
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
