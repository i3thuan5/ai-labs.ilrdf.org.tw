## Purpose

規範本站送到瀏覽器的 HTML 中，允許出現哪些來源的 JavaScript。目的是把可在本站 origin 上執行程式碼的第三方數量降到零，避免 CDN 遭投毒時波及本站使用者。

## ADDED Requirements

### Requirement: 頁面不得載入第三方來源的 JavaScript

本站送出的任何 HTML 頁面 MUST NOT 包含指向本站 origin 以外網域的 `<script src>`。此規則適用於由後端 AI 應用容器產生、但經由本站網域對外提供的頁面。

#### Scenario: AI 應用頁面

- **WHEN** 瀏覽器請求任一 AI 應用路徑（語音辨識、語音合成、翻譯）
- **THEN** 回應的 HTML 中沒有任何指向外部網域的 `<script src>`
- **AND** 特別是不含指向 `cdnjs.cloudflare.com` 的 script

#### Scenario: 網站頁面

- **WHEN** 瀏覽器請求任一由 Django 產生的頁面
- **THEN** 回應的 HTML 中沒有任何指向外部網域的 `<script src>`

### Requirement: 移除第三方 script 後 AI 應用功能不變

移除第三方 script 之後，AI 應用的既有功能 MUST 完全不受影響。

#### Scenario: 語音辨識

- **WHEN** 使用者在語音辨識頁上傳或錄製音檔並送出
- **THEN** 辨識結果正常回傳顯示

#### Scenario: 語音合成

- **WHEN** 使用者在語音合成頁輸入文字並送出
- **THEN** 音訊正常產生並可播放

#### Scenario: 翻譯

- **WHEN** 使用者在翻譯頁輸入文字、切換語言下拉選單並送出
- **THEN** 下拉選單可正常操作，翻譯結果正常回傳

### Requirement: 第三方 script 移除規則失效時可被察覺

用於移除第三方 script 的規則若因上游 HTML 變動而不再命中，該狀況 MUST 能被察覺，而非靜默失效。

#### Scenario: 上游 HTML 改版導致規則失配

- **WHEN** AI 應用升級導致原本的第三方 script 來源不再命中移除規則
- **THEN** 下一次弱點掃描會重新報出 Cross-Domain JavaScript Source File Inclusion 與 Sub Resource Integrity Attribute Missing 兩條告警

#### Scenario: 上游自行改為同源

- **WHEN** AI 應用升級到已把該 script 改為自架同源的版本
- **THEN** 弱點掃描不再報出上述告警，且移除規則可以安全刪除
