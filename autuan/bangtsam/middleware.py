from django.conf import settings


class ContentSecurityPolicyMiddleware:
    """依路徑前綴送出 Content-Security-Policy。

    前台與後台需要不同強度的政策：前台的模板沒有任何 inline script 或
    inline style，可以完全不用 'unsafe-inline'；後台的 inline script 由
    Wagtail 產生，只能放寬。

    這裡不用 django-csp，因為它的 CONTENT_SECURITY_POLICY 設定只能定義
    一條政策，要分路徑只有兩條路：per-view 裝飾器（Wagtail admin 的 view
    不是我們的，套不上），或 EXCLUDE_URL_PREFIXES（那是「該路徑不發
    CSP」，不符合我們對後台的要求）。它真正的強項 nonce 我們現在用不到。

    ── 改用 django-csp 的時機 ──
    一旦需要 nonce（後台要收緊、或 gradio-csp-spike 得出需要 nonce 的
    結論），就改用 django-csp，不要自己實作 nonce。nonce 的安全性取決於
    「用密碼學等級亂數」「每個 request 重新產生」兩件事，做錯不會報錯，
    只會靜默失效成等同 'unsafe-inline'。
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # 上游若已自行送出（例如某個 view 有特殊需求），尊重它，不覆寫。
        if 'Content-Security-Policy' not in response.headers:
            response.headers['Content-Security-Policy'] = \
                self.get_policy(request.path)
        return response

    def get_policy(self, path):
        for prefix in settings.CSP_ADMIN_PATH_PREFIXES:
            if path.startswith(prefix):
                return settings.CSP_POLICY_BACKEND
        return settings.CSP_POLICY_FRONTEND
