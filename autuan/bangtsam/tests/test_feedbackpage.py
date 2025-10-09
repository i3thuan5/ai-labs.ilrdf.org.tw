from wagtail.test.utils import WagtailPageTestCase

from bangtsam.models import FeedbackPage


class FeedbackPageTest(WagtailPageTestCase):

    def test_feedbackurl_blank_then_hide_link_button(self):
        self.page = FeedbackPage(
            title='意見回饋',
            slug="feedback",
        )
        self.assertPageIsRenderable(self.page)

    def test_feedbackurl_exists_then_show_link_button(self):
        pass
