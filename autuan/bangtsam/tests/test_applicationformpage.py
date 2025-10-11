from wagtail.test.utils import WagtailPageTestCase
from wagtail.test.utils.form_data import nested_form_data, streamfield
from wagtail.documents import get_document_model

from bangtsam.models import HomePage, ApplicationFormPage
from bangtsam.tests.utils import tshong_superuser, tshong_wagtail_site
from bangtsam.tests.utils import get_test_document_file


class ApplicationFormPageTest(WagtailPageTestCase):

    @classmethod
    def setUpTestData(cls):
        root = tshong_wagtail_site()
        homepage = HomePage(title="Home")
        root.add_child(instance=homepage)
        cls.homepage = homepage
        cls.superuser = tshong_superuser()

    def test_can_create_ApplicationFormPage_with_none_example_field(self):
        self.client.force_login(self.superuser)
        self.assertCanCreate(
            self.homepage, ApplicationFormPage,
            nested_form_data({
                'title': '申請語料',
                'slug': 'applicationform',
                'sample': streamfield([]),
            })
        )

    def test_can_create_ApplicationFormPage_with_1_example_field(self):
        self.client.force_login(self.superuser)
        fake_file = get_document_model().objects.create(
            title="Mini wav",
            file=get_test_document_file(file_suffix='wav'),
        )
        self.assertCanCreate(
            self.homepage, ApplicationFormPage,
            nested_form_data({
                'title': '申請語料',
                'slug': 'applicationform',
                'sample': streamfield([
                    ('sample_block', {
                        'tribe': 'Pangcah',
                        'sample_text': 'Maranam',
                        'translation_text': '早安。',
                        'audio': fake_file.id,
                    }),
                ]),
            })
        )
