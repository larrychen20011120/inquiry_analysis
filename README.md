# 智慧型醫療期末專案
## 專案名稱與組別
Group3 - 診斷即時搞
## 主要技術支援
* Pyannote Audio: 說話者分離
* Azure Speech: 中文語音辨識
* WMMKS Lab API: 醫療名詞擷取
* SQLite: 儲存相關
* WordCloud Package: 繪製文字雲
* Flask: 架設網站後端服務
* Imgur: 生成文字雲圖片連結

![](/app/static/images/packages.jpg)

## 系統初略架構
![](/app/static/images/system.jpg)

## 使用說明
1. 安裝相關套件 (python3.9)
```
pip install -r requirements.txt
```
2. 申請相關 API 的 KEY 和繁體中文字型並填入`config.py`
* Imgur
* HuggingFace
* WMMKS
* Azure
3. 啟動 web server
```
python manager.py
```
4. 啟動 computing server 在另一個 terminal
```
python server.py
```
5. 在 browser 打上 `127.0.0.1:5000` 即可連上使用

## UI呈現
### 網站登入
![](/app/static/images/web3.png)
### 內部介面
![](/app/static/images/web1.png)
![](/app/static/images/web2.png)
### 文字雲範例
![](/app/static/images/web4.png)

## 註解
`*.dll` 與 `*.exe` 是 server.py 在 windows 下必須下載的文件 (用於處理相關音檔)
Reference: https://github.com/BtbN/FFmpeg-Builds/releases
