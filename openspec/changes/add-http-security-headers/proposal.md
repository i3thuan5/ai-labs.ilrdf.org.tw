## Why

2026-08-05 的 OWASP ZAP 掃描（`kithann/2026-08-05-ZAP-Report-ai-labs.ilrdf.org.tw.html`）對正式站報出 3 個 Medium、3 個 Low。追查後發現缺口全部落在「Django 摸不到的兩條路徑」——nginx 直送的 `/static/`，以及 proxy 到 Gradio 容器的四條 AI 應用路徑。Django 自己那層（`SecurityMiddleware` + `XFrameOptionsMiddleware`）其實已經送出 `X-Frame-Options: DENY`、`X-Content-Type-Options: nosniff`、`Referrer-Policy`、`Cross-Origin-Opener-Policy`，只差 CSP。

本站是對外的族語 AI 公共服務，缺 CSP、缺 anti-clickjacking、以及從 cdnjs 載入未經完整性驗證的第三方 JavaScript，都是實際可被利用的風險面，不只是掃描器噪音。

## What Changes

- nginx 在 server 層統一補上 `X-Content-Type-Options: nosniff`，涵蓋 `/static/`、`/media/` 與所有 proxy 路徑
- nginx 對四條 Gradio location 補上 anti-clickjacking 標頭（Gradio 官方已表態不做，見 design.md）
- Django 前台送出嚴格 CSP（`default-src 'self'`，另放行 YouTube 內嵌），Wagtail 後台送出較寬鬆的 CSP
- nginx 用 `sub_filter` 移除 Gradio HTML 內寫死的 cdnjs `iframeResizer.contentWindow.min.js` script 標籤——該檔案在本站部署下完全多餘（全站以 `<a href>` 連往 AI 應用，無任何 iframe 內嵌）
- 把 `Timestamp Disclosure - Unix` 記錄為誤判並存證，避免下次掃描重複調查

**不在本次範圍內：**

- Gradio 三條路徑的 CSP。Gradio 頁面充滿 inline script/style，寬鬆 CSP 會觸發 ZAP 另一組 Medium（10055-5 / 10055-6），嚴格 CSP 則有上游未解 issue（gradio#7775，dropdown 卡死）。本次不碰，另開 `gradio-csp-spike` 處理
- 升級 Gradio 至 ≥ 6.17.0（上游已把該 script 改為自架）。那三個容器不在本 repo，屬另外三個專案的工作

因此本次目標是 **Medium 3 → 1、Low 3 → 1**，不是歸零。剩下的 1 個 Medium（CSP Header Not Set，Gradio 頁面）由後續 change 處理。

## Capabilities

### New Capabilities

- `http-security-headers`: 各層（nginx 直送、Django 前台、Wagtail 後台、Gradio proxy）應送出哪些 HTTP 安全回應標頭，以及標頭不得重複的規則
- `third-party-script-origin`: 網站送到瀏覽器的 HTML 中，第三方來源 script 的准入規則

### Modified Capabilities

（無。`openspec/specs/` 目前為空，這是本專案第一個 change。）

## Impact

- `nginx/nginx.conf`：新增 server 層 `add_header`、四條 Gradio location 的 `sub_filter` 與 `proxy_set_header Accept-Encoding ""`
- `autuan/autuan/settings.py` / `settings-tsiunnsuann.py`：新增 CSP 設定
- `requirements-prod.in` / `requirements-prod.txt`：可能新增 CSP middleware 相依套件（見 design.md 的取捨）
- `features/`：新增驗收用的 gherkin 情境
- **相依風險**：`sub_filter` 的比對字串與 Gradio 5.49.1 的 HTML 綁定。等 AI 應用升上 Gradio ≥ 6.17.0 後，該規則會靜默失效並成為無害的空操作，屆時應移除
- **無 breaking change**：不改變任何既有 URL、API 或資料結構
