from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


def tshong_superuser():
    superuser = User.objects.create_superuser(
        'kuanliuan', 'kuan@ithuan.tw', 'ku#va0ti17@')
    return superuser


class AutaiTest(TestCase):
    def test_autai_url(self):
        self.client.force_login(tshong_superuser())
        response = self.client.get(
            reverse("adminautai:auth_user_changelist"), follow=True)
        self.assertEqual(response.status_code, 200)
