from django.test import TestCase
from django.urls import reverse
from bangtsam.tests.utils import tshong_superuser


class AutaiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = tshong_superuser()

    def test_autai_url(self):
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("adminautai:auth_user_changelist"), follow=True)
        self.assertContains(
            response,
            '<a href="/kuanli/auth/user/{}/change/">'.format(
                self.superuser.id))
