from wagtail.test.utils import WagtailPageTestCase

from bangtsam.models import HomePage, SitemapPage, \
    IntroPage, FeedbackPage,  ApplicationFormPage, AboutUsPage, \
    CopyrightPage, TermsOfUsePage


class HomePageTest(WagtailPageTestCase):

    def test_can_create_SitemapPage_under_home_page(self):
        self.assertCanCreateAt(HomePage, SitemapPage)

    def test_can_create_IntroPage_under_home_page(self):
        self.assertCanCreateAt(HomePage, IntroPage)

    def test_can_create_FeedbackPage_under_home_page(self):
        self.assertCanCreateAt(HomePage, FeedbackPage)

    def test_can_create_ApplicationFormPage_under_home_page(self):
        self.assertCanCreateAt(HomePage, ApplicationFormPage)

    def test_can_create_AboutUsPage_under_home_page(self):
        self.assertCanCreateAt(HomePage, AboutUsPage)

    def test_can_create_CopyrightPage_under_home_page(self):
        self.assertCanCreateAt(HomePage, CopyrightPage)

    def test_can_create_TermsOfUsePage_under_home_page(self):
        self.assertCanCreateAt(HomePage, TermsOfUsePage)
