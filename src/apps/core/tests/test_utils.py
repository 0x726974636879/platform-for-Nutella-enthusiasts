from unittest.mock import patch

from django.test import TestCase

from apps.core.utils import get_env_variable


class UtilsTest(TestCase):
    def setUp(self):
        self.env = patch.dict("os.environ", {"TEST": "value"})

    def test_value_for_env_variable(self):
        with self.env:
            self.assertEqual(get_env_variable("TEST"), "value")

    def test_error_for_nonexistent_env_variable(self):
        with self.env:
            self.assertRaises(ValueError, get_env_variable, "ERROR")
