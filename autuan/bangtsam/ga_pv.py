"""
GA瀏覽人次（PV）。

逐工頭一个開網頁ê人，會觸發對GA4 Data API查
「GA_PV_START_DATE到昨日」ê PV總和，記佇GA_PV_FILE。
顯示ê時陣，攏提檔案內底ê數字。
"""
import logging
import os
import tempfile
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

logger = logging.getLogger(__name__)

GA_RUN_REPORT_URL = (
    'https://analyticsdata.googleapis.com/v1beta/'
    'properties/{property_id}:runReport'
)
GA_SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
GA_TIMEOUT_SECONDS = 10

# 查GA失敗了後，同一个process等遮久才閣試，
# 免得GA有問題ê時，逐个request攏去等GA。
RETRY_SECONDS = 10 * 60
TSHI_CACHE_KEY = 'ga-pv-tsham-tsing'


def theh_ga_pv():
    """
    提PV總和（int）；檔案無抑是內容毋著，回傳None。
    若檔案毋是今仔日寫ê，先去GA查新ê數字。
    """
    if _ai_tsham_ga():
        try:
            _sia_pv(_tsham_ga_pv())
        except Exception:
            logger.exception('查GA瀏覽人次失敗')
    return _tok_pv()


def _ai_tsham_ga():
    if not settings.GA_PROPERTY_ID or not settings.GA_CREDENTIALS_FILE:
        return False
    if _pv_si_kim_a_jit_e():
        return False
    # cache.add只有頭一擺會成功，鎖同一个process無重複查
    return cache.add(TSHI_CACHE_KEY, True, RETRY_SECONDS)


def _pv_si_kim_a_jit_e():
    try:
        mtime = Path(settings.GA_PV_FILE).stat().st_mtime
    except OSError:
        return False
    sia_jit = datetime.fromtimestamp(
        mtime, tz=timezone.get_current_timezone()).date()
    return sia_jit >= timezone.localdate()


def _tsham_ga_pv():
    # 只有需要查GA ê時才import，無設定GA ê環境免載入
    from google.auth.transport.requests import AuthorizedSession
    from google.oauth2 import service_account

    credentials = service_account.Credentials.from_service_account_file(
        settings.GA_CREDENTIALS_FILE, scopes=GA_SCOPES)
    session = AuthorizedSession(credentials)
    response = session.post(
        GA_RUN_REPORT_URL.format(property_id=settings.GA_PROPERTY_ID),
        json={
            'dateRanges': [{
                'startDate': settings.GA_PV_START_DATE,
                'endDate': 'yesterday',
            }],
            'metrics': [{'name': 'screenPageViews'}],
        },
        timeout=GA_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    rows = response.json().get('rows', [])
    if not rows:
        return 0
    return int(rows[0]['metricValues'][0]['value'])


def _tok_pv():
    try:
        return int(Path(settings.GA_PV_FILE).read_text().strip())
    except (OSError, ValueError):
        return None


def _sia_pv(pv):
    tong = Path(settings.GA_PV_FILE)
    tong.parent.mkdir(parents=True, exist_ok=True)
    # 先寫暫存檔閣換名，免得別个worker讀著寫一半ê檔案
    fd, tmp = tempfile.mkstemp(dir=tong.parent, prefix='.pv-')
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(f'{pv}\n')
        os.replace(tmp, tong)
    except BaseException:
        os.unlink(tmp)
        raise
