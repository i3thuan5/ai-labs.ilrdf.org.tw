// 這是刻意留空的檔案。
//
// Gradio 5.49.1 的內建 template 寫死了一段指向 cdnjs 的 script：
//   https://cdnjs.cloudflare.com/ajax/libs/iframe-resizer/4.3.1/
//   iframeResizer.contentWindow.min.js
// 那支程式只在 Gradio 頁面被別人以 iframe 內嵌時，用來回報高度給 parent。
// 本站一律以 <a href> 連往 AI 應用，沒有任何 iframe 內嵌，所以它完全多餘，
// 卻讓 cdnjs 取得在本站 origin 上執行任意 JavaScript 的能力。
//
// nginx（見 nginx/nginx.conf）以 sub_filter 把那個 URL 換成本檔，
// 讓標籤保持完整、但來源變成同源且沒有任何行為。
//
// Gradio 從 6.17.0 起已改為自架同源，AI 應用升級到該版之後，
// nginx 那條 sub_filter 與本檔都可以一併移除。
