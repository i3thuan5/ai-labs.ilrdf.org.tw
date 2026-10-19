import os
import tempfile
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

from django.core.cache import cache
from django.test import TestCase

from bangtsam.ga_pv import theh_ga_pv, _tsha_ga_pv
from bangtsam.tests.utils import tshong_wagtail_homepage

TSHA_GA = 'bangtsam.ga_pv._tsha_ga_pv'


class GaPvTestCase(TestCase):

    def setUp(self):
        cache.clear()
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        self.pv_file = Path(tmpdir.name) / 'ga-pv' / 'pv.txt'
        self.settings_ga = self.settings(
            GA_PROPERTY_ID='123456789',
            GA_CREDENTIALS_FILE='/run/secrets/ga_credentials',
            GA_PV_FILE=str(self.pv_file),
        )
        self.settings_bo_ga = self.settings(
            GA_PROPERTY_ID='',
            GA_CREDENTIALS_FILE='',
            GA_PV_FILE=str(self.pv_file),
        )

    def sia_tong(self, pv, kui_jit_tsing=0):
        self.pv_file.parent.mkdir(parents=True, exist_ok=True)
        self.pv_file.write_text(f'{pv}\n')
        sikan = time.time() - kui_jit_tsing * 24 * 60 * 60
        os.utime(self.pv_file, (sikan, sikan))


class ThehGaPvTest(GaPvTestCase):

    def test_bo_tong_bo_pv(self):
        with self.settings_bo_ga:
            self.assertIsNone(theh_ga_pv())

    def test_tong_lai_bin_e_pv(self):
        self.sia_tong(359, kui_jit_tsing=3)
        with self.settings_bo_ga:
            self.assertEqual(theh_ga_pv(), 359)

    def test_tong_lai_bin_m_tioh(self):
        self.sia_tong('abc')
        with self.settings_bo_ga:
            self.assertIsNone(theh_ga_pv())

    @patch(tsha_GA)
    def test_bo_setting_ga_bo_tsha(self, tsha_ga):
        self.sia_tong(359, kui_jit_tsing=1)
        with self.settings_bo_ga:
            theh_ga_pv()
        tsha_ga.assert_not_called()

    @patch(tsha_GA, return_value=1000)
    def test_bo_tong_tsha_ga(self, tsha_ga):
        with self.settings_ga:
            self.assertEqual(theh_ga_pv(), 1000)
        self.assertEqual(self.pv_file.read_text(), '1000\n')

    @patch(tsha_GA, return_value=1000)
    def test_tong_si_tsa_hng_e_tsha_ga(self, tsha_ga):
        self.sia_tong(359, kui_jit_tsing=1)
        with self.settings_ga:
            self.assertEqual(theh_ga_pv(), 1000)
        tsha_ga.assert_called_once()

    @patch(tsha_GA, return_value=1000)
    def test_tong_si_kin_a_jit_e_bo_tsha_ga(self, tsha_ga):
        self.sia_tong(359)
        with self.settings_ga:
            self.assertEqual(theh_ga_pv(), 359)
        tsha_ga.assert_not_called()

    @patch(tsha_GA, return_value=1000)
    def test_kang_tsit_jit_kan_na_tsha_tsit_pai(self, tsha_ga):
        with self.settings_ga:
            theh_ga_pv()
            theh_ga_pv()
        tsha_ga.assert_called_once()

    @patch(tsha_GA, side_effect=Exception('GA bo ing'))
    def test_ga_sit_pai_iong_ku_e_pv(self, tsha_ga):
        self.sia_tong(359, kui_jit_tsing=1)
        with self.settings_ga, self.assertLogs('bangtsam.ga_pv', 'ERROR'):
            self.assertEqual(theh_ga_pv(), 359)

    @patch(tsha_GA, side_effect=Exception('GA bo ing'))
    def test_ga_sit_pai_bo_sui_si_koh_tshi(self, tsha_ga):
        self.sia_tong(359, kui_jit_tsing=1)
        with self.settings_ga, self.assertLogs('bangtsam.ga_pv', 'ERROR'):
            theh_ga_pv()
            theh_ga_pv()
        tsha_ga.assert_called_once()


class tshaGaPvTest(GaPvTestCase):

    def tsha(self, response_json):
        response = MagicMock()
        response.json.return_value = response_json
        with self.settings_ga, \
                patch('google.oauth2.service_account.Credentials'
                      '.from_service_account_file') as credentials, \
                patch('google.auth.transport.requests.AuthorizedSession'
                      '.post', return_value=response) as post:
            pv = _tsha_ga_pv()
        return pv, credentials, post

    def test_tsha_tui_khai_si_kau_tsa_hng(self):
        _, credentials, post = self.tsha({'rows': []})
        credentials.assert_called_once_with(
            '/run/secrets/ga_credentials',
            scopes=['https://www.googleapis.com/auth/analytics.readonly'])
        url = post.call_args.args[0]
        self.assertIn('properties/123456789:runReport', url)
        body = post.call_args.kwargs['json']
        self.assertEqual(body['dateRanges'], [
            {'startDate': '2026-09-11', 'endDate': 'yesterday'}])
        self.assertEqual(body['metrics'], [{'name': 'screenPageViews'}])

    def test_thak_pv_tsongho(self):
        pv, _, _ = self.tsha({
            'rows': [{'metricValues': [{'value': '12345'}]}],
        })
        self.assertEqual(pv, 12345)

    def test_bo_tsu_liau_si_0(self):
        pv, _, _ = self.tsha({})
        self.assertEqual(pv, 0)


class GaPvFooterTest(GaPvTestCase):

    def test_footer_hian_si_pv(self):
        homepage = tshong_wagtail_homepage()
        self.sia_tong(12345)
        with self.settings_bo_ga:
            response = self.client.get(homepage.url)
        self.assertContains(response, '瀏覽人次（每日更新）：12345')
        self.assertContains(response, '統計區間：2026/09/11至昨日，每日更新。')

    def test_bo_pv_footer_bo_hian_si(self):
        homepage = tshong_wagtail_homepage()
        with self.settings_bo_ga:
            response = self.client.get(homepage.url)
        self.assertNotContains(response, 'id="ga-pv"')


class GaPvViewTest(GaPvTestCase):

    def test_hue_tuan_pv(self):
        self.sia_tong(12345)
        with self.settings_bo_ga:
            response = self.client.get('/ga-pv/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'pv': 12345})

    def test_bo_pv(self):
        with self.settings_bo_ga:
            response = self.client.get('/ga-pv/')
        self.assertEqual(response.json(), {'pv': None})

    def test_kan_na_GET(self):
        with self.settings_bo_ga:
            response = self.client.post('/ga-pv/')
        self.assertEqual(response.status_code, 405)
