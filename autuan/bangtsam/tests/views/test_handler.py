from unittest.mock import patch, DEFAULT
from django.test import TestCase, override_settings, Client
from django.urls import reverse
from bangtsam.tests.utils import tshong_wagtail_homepage


@override_settings(DEBUG=False)
class TestViewHandler(TestCase):
    def test_handler_renders_404_response(self):
        response = self.client.get('/not-exist/')
        self.assertContains(
            response,
            "頁面可能被刪除、移動，或是網址輸入錯誤。",
            status_code=404
        )

    def test_handler_renders_500_response(self):
        client = Client(raise_request_exception=False)
        with patch("bangtsam.models.HomePage.template",
                   return_value="") as m:
            homepage = tshong_wagtail_homepage()
            response = client.get(homepage.url)
            self.assertContains(
                response,
                "不好意思，伺服器在處理您的請求時遇到了非預期的狀況。",
                status_code=500
            )
