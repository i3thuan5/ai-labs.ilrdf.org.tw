# Sapolita-Website

族語AI成果網站

專案開發枋模

## 開發

### 建立 Python virtual environment

```bash
python -m venv venv
```

### 載入 Python virtual environment

Ta̍k-kái攏ài開，才來開發。

```bash
source venv/bin/activate
```

### 安裝tox

tox是tī本機走test用--ê。

```bash
pip install tox
```

### 更新套件版本

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

### 羅列套件授權類型

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

## 正式機上線

上線時陣愛做：

- 到正式機，複製.env.template，新增環境變數檔`.env`。
- 正式機設定secrets：
  - ./secrets/django_secret_key.txt
  - ./secrets/postgres_passwd.txt
  - ./secrets/sentry_dsn.txt
- 正式機手動migrate：`docker compose exec gunicorn python manage.py migrate`。
- 正式機媒體檔資料夾改權限：`chmod 1777 media/`。
- 正式機新增後台管理員帳號：`docker compose exec gunicorn python manage.py createsuperuser`。
