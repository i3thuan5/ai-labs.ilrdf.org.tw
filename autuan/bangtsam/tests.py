from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


def tshong_superuser():
    superuser = User.objects.create_superuser(
        'kuanliuan', 'kuan@ithuan.tw', 'ku#va0ti17@')
    return superuser


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
