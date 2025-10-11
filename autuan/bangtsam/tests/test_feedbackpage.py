from wagtail.test.utils import WagtailPageTestCase
from wagtail.test.utils.form_data import nested_form_data

from bangtsam.models import HomePage, FeedbackPage
from bangtsam.tests.utils import tshong_superuser, tshong_wagtail_site


class FeedbackPageTest(WagtailPageTestCase):

    @classmethod
    def setUpTestData(cls):
        root = tshong_wagtail_site()
        homepage = HomePage(title="Home")
        root.add_child(instance=homepage)
        cls.homepage = homepage
        cls.superuser = tshong_superuser()

    def test_can_create_feedbackpage_with_blank_feedbackurl(self):
        self.client.force_login(self.superuser)
        self.assertCanCreate(
            self.homepage, FeedbackPage,
            nested_form_data({
                'title': '意見回饋',
                'slug': 'feedback',
            })
        )

    def test_feedbackurl_blank_then_hide_link_button(self):
        page = FeedbackPage(
            title='意見回饋',
            slug="feedback",
            live=True,
        )
        self.homepage.add_child(instance=page)
        response = self.client.get(page.url)
        self.assertNotContains(response, '前往填寫意見回饋表單')

    def test_feedbackurl_exists_then_show_link_button(self):
        page = FeedbackPage(
            title='意見回饋',
            slug="feedback",
            feedbackurl='https://test.com/example-google-form/',
            live=True,
        )
        self.homepage.add_child(instance=page)
        response = self.client.get(page.url)
        self.assertContains(response, '前往填寫意見回饋表單')
