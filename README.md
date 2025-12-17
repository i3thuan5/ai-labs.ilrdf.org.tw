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

利用開源套件[pip-licenses](https://github.com/raimon49/pip-licenses)自動彙整第三方套件授權。請注意，它是利用pip查找本機已安裝的套件資訊，因此應用Docker容器，確保所列出的授權清單與套件清單相對應。

1. 先建立一份Docker映像檔（image）`sapolita-for-licenses`：
   
   ```bash
   docker build -t sapolita-for-licenses .
   ```

2. 用`sapolita-for-licenses`建立Docker容器，安裝並執行pip-licenses：

      ```bash
      docker run --user 0 --rm sapolita-for-licenses:latest /bin/bash -c "pip install pip-licenses && pip-licenses"
      ```

3. 審閱匯出結果：

      ```
      Collecting pip-licenses
      Downloading pip_licenses-5.5.0-py3-none-any.whl.metadata (32 kB)
      Collecting prettytable>=3.12.0 (from pip-licenses)
      [notice] A new release of pip is available: 25.0.1 -> 25.3
      [notice] To update, run: pip install --upgrade pip
      Name                                Version    License                    
      Django                              5.2.7      BSD License            
      Willow                              1.11.0     BSD License
      ...
      anyascii                            0.3.3      ISC License (ISCL)     
      ```

若發現顯示「Unknown」須手動查詢套件授權。

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
