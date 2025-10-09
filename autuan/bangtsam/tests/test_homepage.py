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

    def test_SitemapPage_parent_pages_only_HomePage(self):
        self.assertAllowedParentPageTypes(
            SitemapPage, {HomePage})

    def test_IntroPage_parent_pages_only_HomePage(self):
        self.assertAllowedParentPageTypes(
            IntroPage, {HomePage})

    def test_FeedbackPage_parent_pages_only_HomePage(self):
        self.assertAllowedParentPageTypes(
            FeedbackPage, {HomePage})

    def test_ApplicationFormPage_parent_pages_only_HomePage(self):
        self.assertAllowedParentPageTypes(
            ApplicationFormPage, {HomePage})

    def test_AboutUsPage_parent_pages_only_HomePage(self):
        self.assertAllowedParentPageTypes(
            AboutUsPage, {HomePage})

    def test_CopyrightPage_parent_pages_only_HomePage(self):
        self.assertAllowedParentPageTypes(
            CopyrightPage, {HomePage})

    def test_TermsOfUsePage_parent_pages_only_HomePage(self):
        self.assertAllowedParentPageTypes(
            TermsOfUsePage, {HomePage})
