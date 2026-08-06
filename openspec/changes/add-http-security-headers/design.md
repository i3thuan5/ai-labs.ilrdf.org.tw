## Context

見 proposal.md — Why。以下只補足決定架構所需的現況。

回應由三層產生，各自的標頭現況（取自 ZAP 報告中實際擷取的 response headers）：

```text
                        網際網路
                           │
                 ┌─────────▼──────────┐
                 │  nginx-proxy(外部) │  Strict-Transport-Security ✅
                 └─────────┬──────────┘
                           │
        ┌──────────────────▼───────────────────────┐
        │   nginx  (nginx/nginx.conf ← 本 repo)    │  目前完全沒有 add_header
        └──┬───────────┬────────────────┬──────────┘
  /static/ │           │ /              │ /sapolita/ /sapolita-kaldi/
  /media/  │           │                │ /hnang-kari-ai-asi-sluhay/
           │           │                │ /kari-seejiq-tnpusu-ai-hmjil/
           │           │                │ /favicon.ico
    ┌──────▼──────┐ ┌──▼───────────┐ ┌──▼─────────────┐
    │ staticfiles │ │ gunicorn     │ │ Gradio 5.49.1  │
    │ nginx 直送  │ │ Django 5.2   │ │ 容器 ×4        │
    ├─────────────┤ ├──────────────┤ ├────────────────┤
    │ 標頭：無    │ │ XFO: DENY  ✅│ │ 標頭：無       │
    │             │ │ nosniff    ✅│ │                │
    │             │ │ Referrer   ✅│ │                │
    │             │ │ COOP       ✅│ │                │
    │             │ │ CSP        ❌│ │ 全部 ❌        │
    └─────────────┘ └──────────────┘ └────────────────┘
```

三個關鍵限制：

1. **Gradio 容器不在本 repo。** `docker-compose.yml` 只定義 nginx / gunicorn / django-static / postgres；四個 AI 上游經外部 `ai-labs-bridge` 網路進來，屬另外的專案。本 change 只能從 nginx 這一側處理它們。
2. **Gradio 官方不打算提供標頭設定。** [gradio#8885](https://github.com/gradio-app/gradio/issues/8885)（Ability to set HTTP headers? Clickjacking protection）已被 close as **not planned**。
3. **ZAP 對「弱 CSP」另有一組 Medium 規則。** 只要掛上 CSP 就沒事的直覺是錯的：

   | Rule | 觸發條件 | Risk |
   |---|---|---|
   | 10038 | 完全沒有 CSP 標頭 | Medium |
   | 10055-4 | Wildcard Directive | Medium |
   | 10055-5 | `script-src` 含 `'unsafe-inline'` | Medium |
   | 10055-6 | `style-src` 含 `'unsafe-inline'` | Medium |
   | 10055-10 | `script-src` 含 `'unsafe-eval'` | Medium |

   另注意 ZAP 報告中 CSP 與 X-Content-Type-Options 兩條的 `Instances` 欄位是 `Systemic` 而非數字——列出的 URL 只是樣本，Gradio 頁面同樣中彈，只是沒被印出來。

## Goals / Non-Goals

**Goals:**

- 讓 nginx 成為「補齊上游缺漏標頭」的單一位置，而不是「覆寫所有標頭」的位置
- 前台 CSP 一次到位做到嚴格（ZAP 10055 全過），因為它零成本
- 後台 CSP 以「不擋壞編輯流程」為第一優先
- 移除 cdnjs 的手段要能在失效時被發現

**Non-Goals:**

- 不動 Django 既有已正確送出的標頭（XFO / nosniff / Referrer-Policy / COOP）
- 不在本 change 追求 CSP nonce 或 hash 機制
- 不處理 Gradio 頁面的 CSP（見 Decisions 最後一項）
- 不建立自動化驗收。`features/` 目前沒有任何 step 實作與 `environment.py`，要新增驗收情境等於從零建一套 behave 基礎建設；本次改由本機人工驗證與 ZAP 重掃驗證，自動化另案處理

## Decisions

### D1：CSP 由 Django 送，不由 nginx 送

前台要嚴格、後台要寬鬆，兩者的分界是 URL 前綴（`/katayalan/`、`/kuanli/`）。兩個做法：

| 做法 | 評估 |
|---|---|
| nginx 依 location 分流 | 需為後台新增 location（目前後台是走 `location /` 落到 Django），把路由知識複製到 nginx。日後 Wagtail 改路徑要兩邊同步 |
| **Django middleware 依路徑分流** ✅ | 路由知識留在 Django；未來要上 nonce 時，nonce 必須由產生 HTML 的那一層發，本來就得在 Django |

選 Django。

**為什麼用 `request.path` 前綴，而不是 URL name 或 `resolver_match`**（實作階段查證）：

先排除一個直覺選項——`path('katayalan/', include(wagtailadmin_urls), name='...')` 是行不通的。`include()` 產生的是 `URLResolver`，它連 `.name` 屬性都沒有，Django 會靜靜把 `name` 丟掉。`name` 只能給單一 view 的葉節點。

Django 真正提供的結構化識別是 `request.resolver_match`，但實測後不適用：

| 路徑 | `namespace` | `url_name` |
|---|---|---|
| `/katayalan/login/` | `''` | `wagtailadmin_login` |
| `/kuanli/` | `'adminautai'` | `index` |
| `/katayalan/<不存在>` | `''` | `None` |
| `/kuanli/<不存在>` | `'adminautai'` | `None` |

三個問題：

1. Wagtail admin 沒有設 `app_name`（`namespace` 是空字串），改用 `wagtailadmin_` 名稱前綴慣例。要比對只能綁上游的內部命名，且與 Django admin 的 `namespace` 比對法不一致
2. **後台的 404 頁兩個訊號都消失**：Wagtail 那條 `namespace` 與 `url_name` 皆空，會靜默 fall through 到前台的嚴格政策
3. `resolver_match` 只在 URL 解析成功後才有值；middleware 若在解析前短路（axes 鎖定、redirect middleware）則為 `None`

`request.path` 三種情況都不受影響。代價是前綴字串在 settings 與 urls.py 各有一份，由 `test_admin_path_prefixes_cover_urlconf` 以 `reverse()` 把兩邊繫住——前綴與實際路由不一致時測試會失敗。

### D2：自寫 middleware，不引入 django-csp

`django-csp`（4.0，2025-04，Mozilla MEAO 維護）是這個領域的標準套件。查證其設定模型後，發現它剛好不擅長我們的需求：

- `CONTENT_SECURITY_POLICY` 設定只能定義**一條**政策
- 要分路徑只有兩條路：per-view 裝飾器（Wagtail admin 的 view 不是我們的，套不上），或 `EXCLUDE_URL_PREFIXES`——但後者是「該路徑不發 CSP」，直接違反本 change spec 的「後台送出 CSP」要求
- 它真正的強項 nonce，我們現在用不到（前台零 inline script；後台的 inline script 由 Wagtail 產生，我們無法在其標籤上補 nonce）

我們需要的行為只有「依路徑前綴選一條字串常數並塞進 response」。

選擇在 `bangtsam` 內寫一個約 20 行的 middleware，兩條政策字串定義在 settings，理由：

- 專案風格一致（連 Bootstrap 都自行 vendor，相依套件刻意保持精簡）
- 政策內容在 settings 裡是一眼可讀的字串，審查時不必反推套件的 dict 展開規則
- CSP 標頭發送不涉及密碼學或狀態，自寫的風險面很小

**觸發改用 `django-csp` 的條件**：一旦需要 nonce（例如後台要收緊、或 `gradio-csp-spike` 得出需要 nonce 的結論），就改用套件，不要自己做 nonce。這條寫進 tasks 的註解。

### D3：nginx 只在「上游沒送」的地方補標頭，而不是全域覆寫

`add_header` 有兩個容易踩的性質：

- **會疊加，不會覆寫。** Django 已送 `X-Frame-Options: DENY`，nginx 再 `add_header` 就變成兩個標頭 → 違反 spec 的「安全標頭不得重複」
- **繼承是全有全無。** 只要某個 `location` 自己有任何一條 `add_header`，父層 server 的 `add_header` 全部失效

因此不採「server 層統一加」，改為**逐 location 明確列出**，並在有多條標頭的 location 內把該有的全部寫齊：

| location | nosniff | 防 framing | 備註 |
|---|---|---|---|
| `/static/`、`/media/` | 加 | — | nginx 直送 |
| `/` (Django) | **不加** | **不加** | 上游已送，加了會重複 |
| 四條 Gradio location | 加 | 加 | 兩條都要寫在同一個 location 內。含 ZAP 報告未涵蓋的 `/sapolita/`，四條一律一致處理 |
| `/favicon.ico` | 加 | — | 這條也 proxy 到 Gradio，容易漏 |

一律帶 `always`，讓 4xx/5xx 回應也有標頭。

替代方案「`proxy_hide_header` 把 Django 的標頭藏掉、由 nginx 統一發」被否決：那會讓 `settings.py` 裡的 `SecurityMiddleware` / `XFrameOptionsMiddleware` 變成看似有效實則被丟棄的死設定，是更糟的維護陷阱。

### D4：用 `sub_filter` 移除 cdnjs script，而不是加 `integrity`

那支 script 是 Gradio 5.49.1 的 template 寫死的，無任何設定開關。逐版比對 `js/spa/index.html` 的結果：

```text
 5.49.1 ← 我們在這 ─┐
 6.0.0 / 6.10.0     ├─ <script src="https://cdnjs.cloudflare.com/ajax/libs/
 6.13.0 / 6.16.0    │      iframe-resizer/4.3.1/iframeResizer.contentWindow.min.js" async>
                  ──┘   ✗ 純字面值
────────────────────────────────────────────────────────────────
 6.17.0 ← 上游修掉  ┐  <script src="{{ config.get('root','') }}/static/js/
 6.19 / 6.20 / 6.22 ┴─     iframeResizer.contentWindow.min.js" async>   ✓ 自架同源
```

三個選項的取捨：

| 做法 | 評估 |
|---|---|
| 補 `integrity=` 屬性 | hash 寫死，Gradio 一升版即靜默被擋，故障比現況更難查 |
| 改指向自架的真副本 | 要 vendor 並維護一份我們用不到的函式庫 |
| 整段移除 `<script>` | 需比對整個標籤，牽涉換行與空白，脆弱 |
| **把 URL 換成同源空檔** ✅ | 只比對 URL 這一個明確字串；標籤保持完整；來源變同源且無行為 |

該 script 只在 Gradio 頁面被 iframe 內嵌時才有用，而本站一律以 `<a href>` 連往 AI 應用（`homepage.html`、`main_menu.html`），且 Gradio 頁上的自訂 JS `remove_gradio5_iframe_issue61()` 還會主動刪掉頁面上所有 iframe——它在本站完全多餘。

**為什麼換 URL 而不是整段刪除**（實作階段的修正）：整段刪除要比對 `<script ... async ></script>` 的完整標籤，而該標籤在 Gradio 原始碼中是跨行帶 tab 縮排的，實際送出的位元組無法在無正式站存取的情況下確認。只比對 URL 字串則沒有這個問題——URL 是單一明確 token，且從 Gradio 5.49.1 到 6.16.0 完全一致。

替換目標是 `/static/js/iframe-resizer-noop.js`（隨 Django 靜態檔一起 collect）。同源 script 不會觸發 ZAP 的 SRI 與 Cross-Domain 告警——本次報告中 Django 頁面載入的 `/static/js/bootstrap.bundle.min.js` 等同源 script 全部未被告警，即為佐證。

其餘實作要點：`sub_filter` 比對的是 response body，若上游回壓縮內容就比對不到**且不會報錯**，因此該 location 必須加 `proxy_set_header Accept-Encoding "";`。`nginx:1.28.0-alpine` 官方映像已內建 `ngx_http_sub_module`。

防 framing 選 `X-Frame-Options: DENY` 而非 `SAMEORIGIN`：本站沒有任何內嵌 Gradio 的需求，Gradio 頁面自身的 iframe 也已被前述自訂 JS 刪除，沒有同源內嵌要保留。

### D5：Gradio 頁面的 CSP 排除在本 change 之外

這不是「先做簡單的」，而是這條路目前無解：

```text
  沒有 CSP  ──────────►  10038  CSP Header Not Set          Medium  ✗

  寬鬆 CSP  ──────────►  10055-5  script-src unsafe-inline   Medium  ✗
  ('unsafe-inline')      10055-6  style-src unsafe-inline    Medium  ✗
                         （Gradio 的 <html style="margin:0;…"> 跑不掉）

  嚴格 CSP  ──────────►  ZAP 全過                                    ✓
  (nonce / hash)         但 gradio#7775：dropdown 卡死               ✗
```

[gradio#7775](https://github.com/gradio-app/gradio/issues/7775) 記錄了有人在 nginx 對 Gradio 上 nonce 型 CSP 導致下拉選單卡死，thread 停在 pending clarification，上游沒有解法可抄。在 Gradio 上掛寬鬆 CSP 等於用一個 Medium 換兩個 Medium，淨變差。

因此本 change 的成功標準是 **Medium 3 → 1、Low 3 → 1**，剩下那個 Medium 移交 `gradio-csp-spike`。這個切法讓本 change 得以獨立驗證與上線，不被一個結果未知的探索卡住。

## Risks / Trade-offs

- **`sub_filter` 與 Gradio HTML 版本耦合，且失效時是靜默的** → 只比對 URL 這一個明確字串（而非整個標籤）已大幅降低失配機率；殘餘風險由定期 ZAP 掃描承接：規則一旦失配，Cross-Domain JavaScript 與 SRI 兩條告警會重新出現。代價是察覺延遲取決於掃描頻率，而非部署當下即時得知
- **`Accept-Encoding ""` 讓 nginx 與上游之間改走明文，nginx 需自行重新壓縮** → 只影響四條 AI 應用路徑的 HTML 首頁回應（`sub_filter_types` 預設只吃 `text/html`），資產檔不受影響，成本可忽略
- **前台嚴格 CSP 可能擋到 CMS 內文裡編輯者貼進來的內容** → 目前 `EmbedBlock` 實際只用於 YouTube，但 oEmbed 本身不限供應商。上線前需檢視 CMS 既有內容實際用到的 embed 來源（見 Open Questions）
- **後台 CSP 若放太寬等同沒做** → 接受。後台需登入，未認證掃描掃不到，本 change 對它的目標是縱深防禦而非清除告警；收緊留待後續
- **自寫 middleware 少了套件的社群檢視** → 以 D2 的觸發條件控制：一旦需要 nonce 就換套件

## Migration Plan

1. 本機起 `docker compose`，逐項以 `curl -I` 驗標頭、以 `curl -s | grep` 驗外部 script 已消失
2. 人工走完前台（主選單下拉、目錄跳轉、圖片燈箱、YouTube 影片）與後台（登入、StreamField 編輯、圖片與文件上傳、發布），開瀏覽器主控台確認無 CSP 違規
3. 人工走完三個 AI 應用的核心流程（辨識、合成、翻譯含語言下拉），確認移除 script 沒有副作用
4. 部署後重跑一次 ZAP，確認 Medium 3 → 1、Low 3 → 1

**回滾**：本 change 只動 `nginx/nginx.conf` 與 Django 設定。nginx 部分還原檔案後 `docker compose restart nginx` 即可；CSP 部分可先把 middleware 從 `MIDDLEWARE` 移除再重啟，不需要資料庫或資產變更。

## Open Questions

- CMS 既有內容實際用到哪些 oEmbed 供應商？決定前台 CSP 的 `frame-src` 白名單要列哪些網域。可在實作階段直接查 CMS 內容得知，不影響本文件的任何決策或 spec
