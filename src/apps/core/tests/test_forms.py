from django.test import TestCase

from apps.core.forms import LoginForm, SearchUserForm, SignUpForm


class LoginFormTest(TestCase):
    def setUp(self):
        self.credentials = {"email": "charlemagne@free.fr", "password": "1234"}

    def test_login_form_field_labels(self):
        form = LoginForm()
        self.assertTrue(form.fields["email"].label == "Adresse email")
        self.assertTrue(form.fields["password"].label == "Mot de passe")

    def test_login_form_field_help_texts(self):
        form = LoginForm()
        self.assertEqual(
            form.fields["email"].help_text, "Entrez une adresse email valide."
        )
        self.assertEqual(
            form.fields["password"].help_text, "Entrez votre mot de passe."
        )

    def test_login_form(self):
        form = LoginForm(data=self.credentials)
        self.assertTrue(form.is_valid())

    def test_login_form_without_password(self):
        credentials_ = self.credentials.copy()
        del credentials_["password"]
        form = LoginForm(data=credentials_)
        self.assertFalse(form.is_valid())

    def test_login_form_email_invalid(self):
        credentials_ = self.credentials.copy()
        credentials_["email"] = "charlemagne"
        form = LoginForm(data=credentials_)
        self.assertFalse(form.is_valid())

    def test_login_form_email_too_long(self):
        credentials_ = self.credentials.copy()
        credentials_["email"] = f"{250 * 'a'}@free.fr"
        form = LoginForm(data=credentials_)
        self.assertFalse(form.is_valid())


class SignUpFormTest(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "Albert",
            "first_name": "Patrick",
            "last_name": "PDA",
            "email": "ppda@free.fr",
            "password1": "thisIsaPassword1",
            "password2": "thisIsaPassword1"
        }

    def test_signup_form_field_labels(self):
        form = SignUpForm()
        self.assertTrue(form.fields["username"].label == "Pseudo")
        self.assertTrue(form.fields["first_name"].label == "Prenom")
        self.assertTrue(form.fields["last_name"].label == "Nom")
        self.assertTrue(form.fields["email"].label == "Adresse email")
        self.assertTrue(form.fields["password1"].label == "Mot de passe")
        self.assertTrue(
            form.fields["password2"].label == "Verification de mot de passe."
        )

    def test_signup_form_field_help_texts(self):
        form = SignUpForm()
        self.assertEqual(
            form.fields["username"].help_text, "Entrez votre pseudo."
        )
        self.assertEqual(
            form.fields["first_name"].help_text, "Entrez votre prenom."
        )
        self.assertEqual(
            form.fields["last_name"].help_text, "Entrez votre nom."
        )
        self.assertEqual(
            form.fields["email"].help_text, "Entrez une adresse email valide."
        )
        self.assertEqual(
            form.fields["password1"].help_text, "Entrez votre mot de passe."
        )
        self.assertEqual(
            form.fields["password2"].help_text,
            "Entrez le même mot de passe que ci-dessus, pour vérification."
        )

    def test_signup_form(self):
        form = SignUpForm(data=self.credentials)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_signup_form_without_password_verification(self):
        credentials_ = self.credentials.copy()
        del credentials_["password2"]
        form = SignUpForm(data=credentials_)
        self.assertFalse(form.is_valid())

    def test_signup_form_with_bad_password_verification(self):
        credentials_ = self.credentials.copy()
        credentials_["password2"] = "4567"
        form = SignUpForm(data=credentials_)
        self.assertFalse(form.is_valid())

    def test_signup_form_without_email(self):
        credentials_ = self.credentials.copy()
        del credentials_["email"]
        form = SignUpForm(data=credentials_)
        self.assertFalse(form.is_valid())

    def test_signup_form_email_invalid(self):
        credentials_ = self.credentials.copy()
        credentials_["email"] = "charlemagne"
        form = SignUpForm(data=credentials_)
        self.assertFalse(form.is_valid())

    def test_signup_form_email_too_long(self):
        credentials_ = self.credentials.copy()
        credentials_["email"] = f"{250 * 'a'}@free.fr"
        form = LoginForm(data=credentials_)
        self.assertFalse(form.is_valid())

    def test_signup_form_first_name_too_long(self):
        credentials_ = self.credentials.copy()
        credentials_["first_name"] = f"{31 * 'a'}"
        form = LoginForm(data=credentials_)
        self.assertFalse(form.is_valid())

    def test_signup_form_last_name_too_long(self):
        credentials_ = self.credentials.copy()
        credentials_["first_name"] = f"{31 * 'a'}"
        form = LoginForm(data=credentials_)
        self.assertFalse(form.is_valid())


class SearchUserFormTest(TestCase):
    def setUp(self):
        # User to find.
        self.user_to_find = {"username": "Patrick"}

    def test_searchuser_form_field_labels(self):
        form = SearchUserForm()
        self.assertTrue(form.fields["username"].label == "Utilisateur")

    def test_searchuser_form_field_help_texts(self):
        form = SearchUserForm()
        self.assertEqual(
            form.fields["username"].help_text, "Rechercher un utilisateur"
        )

    def test_searchuser_form(self):
        form = SearchUserForm(data=self.user_to_find)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_searchuser_form_without_username(self):
        user_to_find = {}
        form = SearchUserForm(data=user_to_find)
        self.assertFalse(form.is_valid())

    def test_searchuser_form_username_too_long(self):
        user_to_find_ = self.user_to_find.copy()
        user_to_find_["username"] = f"{31 * 'a'}"
        form = SearchUserForm(data=user_to_find_)
        self.assertFalse(form.is_valid())
