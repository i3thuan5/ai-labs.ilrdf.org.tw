# ai-labs.ilrdf.org.tw

族語AI成果網站。上線指令：

```bash
docker compose -p ai-labs.ilrdf.org.tw \
  -f deploy/docker-compose-ai-labs.yml \
  -f deploy/docker-compose-formosan-ai.yml \
  up -d --pull
```

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

### 第三方套件

請見[第三方套件資訊.md](te-sann-hong.md)。

## 正式機上線

上線前愛做：

- 到正式機，複製.env.template，新增環境變數檔`.env`。
- 正式機設定secrets：
  - ./secrets/django_secret_key.txt
  - ./secrets/postgres_passwd.txt
  - ./secrets/sentry_dsn.txt
- 正式機媒體檔資料夾改權限：`chmod 1777 media/`。
- 開[https://github.com/i3thuan5/Formosan-AI](https://github.com/i3thuan5/Formosan-AI) ê docker compose服務。

上線後愛做：

- 正式機手動migrate：`docker compose exec gunicorn python manage.py migrate`。
- 正式機新增後台管理員帳號：`docker compose exec gunicorn python manage.py createsuperuser`。

定期更新憑證：

由於原語會每次提供檔案不同，因此要特別注意，除了 .crt 之外，還需要有 root.cer, uca1.cer, uca2.cer，才能產生完整的憑證鍊。

以 20270127 到期的憑證為例：

```bash
cat ILRDFServer.crt uca_1.cer uca_2.cer root.cer > ilrdf.org.tw.2026.chained.crt
cp ILRDFServer.key ilrdf.org.tw.2026.key
```

用 scp 上傳到 diyong3 主機後，先備份現有憑證

```bash
cd git/Zugi
docker cp zugi-nginx-proxy-1:/etc/nginx/certs/ilrdf.org.tw.key ~/ilrdf.org.tw.old.key
docker cp zugi-nginx-proxy-1:/etc/nginx/certs/ilrdf.org.tw.crt ~/ilrdf.org.tw.old.chained.crt
```

再寫入新憑證

```bash
docker cp ~/ilrdf.org.tw.2026.key zugi-nginx-proxy-1:/etc/nginx/certs/ilrdf.org.tw.key
docker cp ~/ilrdf.org.tw.2026.chained.crt zugi-nginx-proxy-1:/etc/nginx/certs/ilrdf.org.tw.crt
```

最後重啟 nginx

```bash
docker compose exec nginx-proxy nginx -s reload
```
