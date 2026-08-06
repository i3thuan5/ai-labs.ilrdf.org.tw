## 1. 現況確認

- [x] 1.1 查 CMS 既有內容實際用到的 oEmbed 供應商網域，決定前台 CSP `frame-src` 白名單（design.md — Open Questions）
- [x] 1.2 清點 `nginx.conf` 中所有 proxy 到 Gradio 的 location，確認四條 AI 應用路徑加 `/favicon.ico` 全部列入，不因 ZAP 報告未涵蓋 `/sapolita/` 而漏掉它
- [x] 1.3 記錄目前正式站的標頭基準線，供改完後比對

## 2. Django CSP middleware

- [x] 2.1 在 `autuan/autuan/settings.py` 新增兩條政策字串設定：前台嚴格版（`default-src 'self'`，`script-src` 不含 `'unsafe-inline'` / `'unsafe-eval'` / 萬用字元，`frame-src` 帶 1.1 查到的白名單）與後台寬鬆版
- [x] 2.2 在 `autuan/bangtsam/` 新增 middleware，依 URL 前綴（`/katayalan/`、`/kuanli/` 走後台版，其餘走前台版）送出 `Content-Security-Policy`
- [x] 2.3 在 middleware 原始碼加註解說明 design.md D2 的取捨與「需要 nonce 時改用 `django-csp`」的觸發條件
- [x] 2.4 把 middleware 加進 `settings.py` 的 `MIDDLEWARE`
- [x] 2.5 在 `autuan/bangtsam/tests/` 新增測試：前台頁面回應含 CSP 且 `script-src` 不含 `'unsafe-inline'` / `'unsafe-eval'` / `*`；後台路徑回應含 CSP

## 3. nginx 補齊缺漏標頭

- [x] 3.1 `nginx/nginx.conf` 的 `/static/`、`/media/` 各加 `add_header X-Content-Type-Options nosniff always;`
- [x] 3.2 四條 Gradio location（`/sapolita/`、`/sapolita-kaldi/`、`/hnang-kari-ai-asi-sluhay/`、`/kari-seejiq-tnpusu-ai-hmjil/`）各加 nosniff 與防 framing 標頭，兩條都要寫在同一個 location 內
- [x] 3.3 `/favicon.ico` location 補 nosniff（這條也 proxy 到 Gradio，容易漏）
- [x] 3.4 確認 `location /` 沒有加任何 `add_header`，避免與 Django 既有標頭重複
- [ ] 3.5 `tox -e checknginx` 通過

## 4. nginx 移除 cdnjs script

- [x] 4.1 取得 cdnjs script 的精確 URL（來源：ZAP 報告的 Evidence 欄位，並與 Gradio 5.49.1 原始碼核對一致）
- [x] 4.2 四條 Gradio location 各加 `proxy_set_header Accept-Encoding "";` 與 `sub_filter` 規則，把該 URL 換成同源的 `/static/js/iframe-resizer-noop.js`（新增該空檔）
- [x] 4.3 在 `nginx.conf` 加註解：本規則綁定 Gradio 5.49.1，上游 6.17.0 起已改為自架同源，AI 應用升級後應移除本規則
- [ ] 4.4 `tox -e checknginx` 通過

## 5. 自動化驗收（本次不做）

`features/` 目前只有一個沒有 scenario 的範例檔，沒有 step 實作也沒有
`environment.py`，新增驗收情境等於從零建一套 behave 基礎建設，超出本 change
範圍；情境有了而 step 沒有，還會讓現在會過的 `tox -e behave` 反而失敗。

驗證改由第 6 節的本機人工驗證與 7.3 的 ZAP 重掃負責。自動化驗收另案處理。

## 6. 本機人工驗證

- [ ] 6.1 起 `docker compose`，以 `curl -I` 逐條路徑核對標頭，確認無重複標頭
- [ ] 6.2 走前台：主選單下拉、目錄跳轉、圖片放大燈箱、內文 YouTube 影片，主控台無 CSP 違規
- [ ] 6.3 走後台：登入、編輯 StreamField、上傳圖片與文件、發布頁面，全部正常完成
- [ ] 6.4 走三個 AI 應用：語音辨識送出音檔、語音合成產生音訊、翻譯切換語言下拉並送出，功能與移除 script 前一致

## 7. 收尾

- [x] 7.1 在 `kithann/` 建立掃描誤判存證，記錄 `Timestamp Disclosure - Unix` 為誤判（`1610616832` = `0x60000000`、`1744830465` = `0x68000001`，係 React fiber lane 常數而非時間戳）
- [x] 7.2 `tox -e test`、`tox -e flake8`、`tox -e pymarkdown`、`tox -e checkdeploy` 全部通過
- [ ] 7.3 部署後重跑 ZAP，確認 Medium 3 → 1、Low 3 → 1，且未出現 10055-4 / 10055-5 / 10055-6 / 10055-10 等新的弱 CSP 告警
- [ ] 7.4 確認剩下的 1 個 Medium（CSP Header Not Set，Gradio 頁面）已登記在 `gradio-csp-spike`
