

# PM2.5 即時監測系統

本專案使用 Python 串接環境部開放資料 API，取得各縣市測站的 PM2.5 最新資料。

## 功能

- 使用者輸入環境部 API Key
- 查看可監測縣市
- 自行選擇及更改預設城市
- 每 15 分鐘自動更新
- 每個測站只保留最新一筆資料
- PM2.5 超過警戒值時發出警示音
- 輸入 `stop` 停止監測
- 輸入 `shutdown` 關閉程式

## 安裝

```bash
pip install -r requirements.txt

## API可以自己去申請就好
https://airtw.moenv.gov.tw/
