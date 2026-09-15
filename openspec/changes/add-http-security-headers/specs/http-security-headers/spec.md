## Purpose

規範本站對外送出的 HTTP 安全回應標頭：不論該回應由 nginx 直接送出、由 Django/Wagtail 產生、或由後端 AI 應用容器產生，瀏覽器收到的標頭都必須一致且完整。

## ADDED Requirements

### Requirement: 所有回應皆送出 MIME 類型嗅探防護

本站對外的每一個 HTTP 回應 MUST 包含 `X-Content-Type-Options: nosniff`，不因該回應由哪一層產生而有差異。

#### Scenario: 靜態檔案

- **WHEN** 瀏覽器請求 `/static/` 或 `/media/` 下的任一檔案
- **THEN** 回應包含 `X-Content-Type-Options: nosniff`

#### Scenario: AI 應用頁面

- **WHEN** 瀏覽器請求任一 AI 應用路徑（語音辨識、語音合成、翻譯）
- **THEN** 回應包含 `X-Content-Type-Options: nosniff`

#### Scenario: 網站頁面

- **WHEN** 瀏覽器請求首頁、計畫介紹或其他內容頁
- **THEN** 回應包含 `X-Content-Type-Options: nosniff`

### Requirement: AI 應用頁面防止被跨站內嵌

AI 應用路徑的回應 MUST 送出可防止被第三方網站以 frame 內嵌的標頭（`X-Frame-Options` 或 CSP `frame-ancestors` 擇一即可）。

#### Scenario: AI 應用頁面被第三方內嵌

- **WHEN** 第三方網站嘗試以 `<iframe>` 載入任一 AI 應用路徑
- **THEN** 瀏覽器拒絕算繪該 frame

### Requirement: 安全標頭不得重複

同一個回應中，同一個安全標頭 MUST 只出現一次。已由上游應用送出該標頭的路徑，代理層 MUST NOT 再次附加。

#### Scenario: 網站頁面已由應用送出防內嵌標頭

- **WHEN** 瀏覽器請求由 Django 產生的頁面
- **THEN** 回應中 `X-Frame-Options` 僅出現一次

### Requirement: 網站前台送出嚴格內容安全政策

由 Django 產生的公開頁面 MUST 送出 `Content-Security-Policy` 標頭。該政策 MUST NOT 在 `script-src` 中使用 `'unsafe-inline'`、`'unsafe-eval'` 或萬用字元來源。

#### Scenario: 公開頁面

- **WHEN** 瀏覽器請求首頁、計畫介紹、網站導覽或版權頁
- **THEN** 回應包含 `Content-Security-Policy` 標頭
- **AND** 該政策的 `script-src` 不含 `'unsafe-inline'`、`'unsafe-eval'` 或 `*`

#### Scenario: 前台既有功能不受影響

- **WHEN** 使用者在啟用 CSP 的前台頁面操作主選單下拉、目錄跳轉與圖片放大燈箱
- **THEN** 功能正常運作，且瀏覽器主控台沒有 CSP 違規訊息

#### Scenario: 內文嵌入的 YouTube 影片

- **WHEN** 頁面內文含有嵌入的 YouTube 影片
- **THEN** 該影片正常載入播放

### Requirement: 內容管理後台送出內容安全政策

Wagtail 內容管理後台的頁面 MUST 送出 `Content-Security-Policy` 標頭。該政策得放寬至足以讓後台正常運作。

#### Scenario: 後台頁面

- **WHEN** 已登入的編輯者瀏覽後台任一頁面
- **THEN** 回應包含 `Content-Security-Policy` 標頭

#### Scenario: 後台編輯功能不受影響

- **WHEN** 編輯者登入、編輯 StreamField 內容、上傳圖片與文件、並發布頁面
- **THEN** 所有操作正常完成
