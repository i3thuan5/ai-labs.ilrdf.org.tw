from wagtail.models import Page
from wagtail.test.utils import WagtailPageTestCase
from wagtail.test.utils.form_data import nested_form_data, streamfield

from bangtsam.models import RichTextBasePage, HomePage
from bangtsam.tests.utils import tshong_superuser


class TestPage(RichTextBasePage):
    template = 'bangtsam/richtextbase.html'


class KongkeIahFormTest(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root_page = Page.objects.live().first()
        cls.superuser = tshong_superuser()

    def test_OK_can_create_page_with_valid_slug(self):
        self.client.force_login(self.superuser)
        self.assertCanCreate(
            self.root_page, HomePage,
            nested_form_data({
                'title': '計畫介紹',
                'slug': 'halaka-ato-nitayalan',
                'body': streamfield([])
            })
        )

    def test_clean_sitpai_slug(self):
        self.client.force_login(self.superuser)
        with self.assertRaises(AssertionError):
            self.assertCanCreate(
                self.root_page, HomePage,
                nested_form_data({
                    'title': '計畫介紹',
                    'slug': '介紹',
                    'body': streamfield([])
                })
            )
