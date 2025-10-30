from django.test import TestCase, override_settings


@override_settings(DEBUG=False)
class TestViewHandle404(TestCase):
    def test_handler_renders_404_response(self):
        response = self.client.get('/not-exist/')
        self.assertContains(
            response,
            "頁面可能被刪除、移動，或是網址輸入錯誤。",
            status_code=404
        )
