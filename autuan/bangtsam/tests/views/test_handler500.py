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
            "不好意思，伺服器在處理您的請求時遇到了非預期的狀況。",
            status_code=500
        )
