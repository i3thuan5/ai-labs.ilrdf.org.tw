from django.test import TestCase
from django.conf import settings
from wagtail.test.utils import WagtailPageTestCase

from bangtsam.models import IntroPage, SitemapPage
from bangtsam.tests.utils import tshong_wagtail_homepage


class ThehWagtailPagesTest(WagtailPageTestCase):

    def test_theh_wagtail_pages_into_template(self):
        homepage = tshong_wagtail_homepage()
        response = self.client.get(homepage.url)
        self.assertEqual(response.context['homepage'], homepage)
        self.assertEqual(response.context['sitemappage'], None)
        self.assertEqual(response.context['intropage'], None)
        self.assertEqual(response.context['feedbackpage'], None)
        self.assertEqual(response.context['applicationformpage'], None)
        self.assertEqual(response.context['termofusepage'], None)
        self.assertEqual(response.context['copyrightpage'], None)

    def test_page_must_be_live(self):
        homepage = tshong_wagtail_homepage()
        homepage.add_child(
            instance=IntroPage(
                title='計畫介紹', slug='intro', live=False
            )
        )
        homepage.add_child(
            instance=SitemapPage(
                title='網站地圖', slug='sitemap', live=True
            )
        )
        response = self.client.get(homepage.url)
        self.assertNotContains(response, '/introslug/')
        self.assertContains(response, '/sitemap/')


class ThehAiWebsiteURLTest(TestCase):

    def test_theh_ai_url_into_template(self):
        homepage = tshong_wagtail_homepage()
        response = self.client.get(homepage.url)
        self.assertContains(
            response, settings.SAPOLITA_ASR_URL)
        self.assertContains(
            response, settings.SAPOLITA_TTS_URL)
        self.assertContains(
            response, settings.SAPOLITA_TRANSLATE_URL)


class ThehGaIdTest(TestCase):

    def test_bo_setting_tio_bo_ga(self):
        homepage = tshong_wagtail_homepage()
        with self.settings(GA_MEASUREMENT_ID=''):
            response = self.client.get(homepage.url)
        self.assertNotContains(response, 'googletagmanager.com')

    def test_u_setting_tio_u_ga(self):
        homepage = tshong_wagtail_homepage()
        with self.settings(GA_MEASUREMENT_ID='G-TESTING000'):
            response = self.client.get(homepage.url)
        self.assertContains(response, 'G-TESTING000')
