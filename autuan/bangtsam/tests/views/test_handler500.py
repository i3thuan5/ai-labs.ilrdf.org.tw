from django.test import TestCase, override_settings
from django.test import Client
from django.urls import path

from bangtsam.urls import urlpatterns


def problematic_view(request):
    raise Exception("Simulating a server error for testing handler500")


urlpatterns += [
    path('problematic/', problematic_view),
]

handler500 = "bangtsam.views.handle500"


@override_settings(DEBUG=False, ROOT_URLCONF=__name__)
class TestViewHandler(TestCase):
    def test_handler_renders_500_response(self):
        client = Client(raise_request_exception=False)
        response = client.get('/problematic/')
        self.assertContains(
            response,
            "頁面可能被刪除、移動，或是網址輸入錯誤。",
            status_code=500
        )
