# Sapolita-Website

族語AI成果網站

專案開發枋模

## 建立 Python virtual environment

```bash
python -m venv venv
```

## 載入 Python virtual environment

Ta̍k-kái攏ài開，才來開發。

```bash
source venv/bin/activate
```

## 安裝tox

tox是tī本機走test用--ê。

```bash
pip install tox
```

## 更新套件版本

`requirements-dev.in`是記專案有直接用ê第三方套件。`requirements-dev.txt`是管kui專案全部第三方套件koh對應版本，保證開發、CI試驗、上線版本一致。

1. 請先 `pip install pip-tools` tàu [pip-tools](https://github.com/jazzband/pip-tools) 自動管理套件版本。
2. 手動更新`requirements-dev.in`。
3. 揀一款指令自動更新套件版本。

      ```bash
      # 有必要--ê才更新
      pip-compile
      # 盡量更新
      pip-compile --upgrade
      ```

4. 檢查`requirements-dev.txt`更新狀態。

## 羅列套件授權類型

`pip-licenses.txt`是記專案有用的第三方套件授權，是利用[pip-licenses](https://github.com/raimon49/pip-licenses)自動彙整。請注意，它是利用pip查找本機已安裝的套件資訊，因此請確認本機僅安裝專案有用的套件再利用pip-licenses。

1. 先安裝pip-licenses：

      ```bash
      pip install pip-licenses
      ```

2. 列出專案的第三方套件授權：

      ```bash
      pip-licenses > licenses-of-requirements.txt
      ```

3. 人工審閱匯出結果，若發現顯示「Unknown」須手動查詢套件授權並回填。

## 產生favicon.ico

1. 繪製SVG格式的favicon原圖
2. 開終端機，用`convert`指令轉出各尺寸的PNG：

      ```bash
      convert -background transparent -define 'icon:auto-resize=32' logo.svg favicon.ico
      convert -size 180x180 logo.svg apple-touch-icon.png
      convert -size 192x192 logo.svg icon-192.png
      convert -size 512x512 logo.svg icon-512.png
      ```

## 色盤

主色調：

- 橘  #D04410
- 亮橘 #F4855D
- 暗橘 #AC370C

附加色調：

- 紅 #D10000
- 暗紅 #AD0001
- 藍 #2F5ACB
- 暗藍 #274DAB
- 白 #FFFFFF

用於：

- 橘：主選單背景色、橘按鈕初始狀態背景色
- 亮橘：橘按鈕聚焦狀態邊框色
- 暗橘：超連結字色、橘按鈕滑過狀態背景色
- 藍：超連結滑過狀態字色、藍按鈕初始狀態背景色
- 暗藍：藍按鈕滑過狀態背景色
- 紅：紅按鈕初始狀態背景色
- 暗紅：紅按鈕滑過狀態背景色
- 白：主選單按鈕字色、內文背景色
