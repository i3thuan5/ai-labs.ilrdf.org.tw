from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from wagtail.test.utils import WagtailPageTestCase

from bangtsam.tests.utils import tshong_superuser, tshong_wagtail_homepage


def get_directive(policy, name):
    for directive in policy.split(';'):
        directive = directive.strip()
        if directive.split(' ')[0] == name:
            return directive
    return None


class FrontendCspTest(WagtailPageTestCase):

    def setUp(self):
        self.homepage = tshong_wagtail_homepage()

    def test_frontend_has_csp(self):
        response = self.client.get(self.homepage.url)
        self.assertIn('Content-Security-Policy', response.headers)

    def test_frontend_script_src_has_no_unsafe_sources(self):
        response = self.client.get(self.homepage.url)
        script_src = get_directive(
            response.headers['Content-Security-Policy'], 'script-src')
        self.assertIsNotNone(script_src)
        self.assertNotIn("'unsafe-inline'", script_src)
        self.assertNotIn("'unsafe-eval'", script_src)
        self.assertNotIn('*', script_src)

    def test_frontend_defines_directives_without_fallback(self):
        # frame-ancestors、form-action、base-uri 不會 fallback 到 default-src，
        # 沒有明寫的話 ZAP 會判為 Wildcard Directive。
        policy = self.client.get(
            self.homepage.url).headers['Content-Security-Policy']
        for name in ('frame-ancestors', 'form-action', 'base-uri'):
            self.assertIsNotNone(
                get_directive(policy, name), f'欠 {name}')

    def test_frontend_allows_youtube_embed(self):
        response = self.client.get(self.homepage.url)
        frame_src = get_directive(
            response.headers['Content-Security-Policy'], 'frame-src')
        self.assertIn('https://www.youtube.com', frame_src)


class AdminCspTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.superuser = tshong_superuser()

    def test_wagtail_admin_has_csp(self):
        # 用登入頁而不是 dashboard：dashboard 需要有 Site 才跑得起來，
        # 這條測試要驗的是 /katayalan/ 這個前綴，沒必要牽涉 Site 狀態。
        response = self.client.get(reverse('wagtailadmin_login'))
        self.assertIn('Content-Security-Policy', response.headers)

    def test_django_admin_has_csp(self):
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse('adminautai:auth_user_changelist'), follow=True)
        self.assertIn('Content-Security-Policy', response.headers)

    def test_admin_path_prefixes_cover_urlconf(self):
        # CSP_ADMIN_PATH_PREFIXES 是硬寫的字串，urls.py 改路徑時不會跟著改。
        # 這條把兩邊繫在一起：後台網址若不在任何一個前綴內，測試就會失敗。
        #
        # 沒有改用 resolver_match 的 namespace / url_name 來對應，是因為
        # Wagtail admin 沒有設 app_name（namespace 是空字串），
        # 而且後台的 404 頁 url_name 也是 None，兩個訊號都沒有，
        # 會靜默掉到前台的嚴格政策。request.path 沒有這個漏洞。
        for name in ('wagtailadmin_home', 'adminautai:index'):
            url = reverse(name)
            covered = False
            for prefix in settings.CSP_ADMIN_PATH_PREFIXES:
                if url.startswith(prefix):
                    covered = True
            self.assertTrue(
                covered, f'{name}（{url}）不在 CSP_ADMIN_PATH_PREFIXES 內')

    def test_admin_csp_differs_from_frontend(self):
        admin_policy = self.client.get(
            reverse('wagtailadmin_login')
        ).headers['Content-Security-Policy']
        script_src = get_directive(admin_policy, 'script-src')
        self.assertIn("'unsafe-inline'", script_src)
