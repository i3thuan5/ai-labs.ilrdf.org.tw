# 第三方套件資訊

## 後端套件授權資訊

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

      ```txt
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

## 前端套件授權資訊

無法用自動化方式羅列，為手動列出。若前端套件有增減，請更新以下表格。

|Name|Version|License|
|--|--|--|
|bootstrap|5.2.3|MIT license|
|TauhuOo20.05-Regular|20.05|SIL Open Font License 1.1|
