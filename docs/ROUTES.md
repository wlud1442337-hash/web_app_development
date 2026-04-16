# 路由設計文件 (Routes Design)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁與操作入口 | GET | `/` | `index.html` | 首頁，提供開始抽籤的按鈕與系統介紹 |
| 執行抽籤邏輯 | POST | `/draw` | — | 隨機產生結果，若登入則寫入紀錄，重導向至結果頁 |
| 檢視單次結果 | GET | `/result/<id>` | `result.html` | 呈現特定紀錄的抽籤結果與解籤資訊 |
| 註冊頁面 | GET | `/register` | `login.html` | 顯示會員註冊表單 |
| 註冊送出 | POST | `/register` | — | 處理註冊資料，寫入 DB，成功重導向至登入 |
| 登入頁面 | GET | `/login` | `login.html` | 顯示登入表單 |
| 登入送出 | POST | `/login` | — | 驗證帳號密碼，設定 Session，重導向至首頁 |
| 登出 | GET | `/logout` | — | 清除 Session，重導向至首頁 |
| 歷史紀錄列表 | GET | `/history` | `history.html` | 列出目前登入使用者的過往抽籤紀錄 |
| 香油錢捐獻頁面 | GET | `/donate` | `donate.html` | 顯示模擬捐獻表單 |
| 送出模擬捐獻 | POST | `/donate` | — | 將捐獻資料寫入 DB，重導至感謝通知或首頁 |

## 2. 每個路由的詳細說明

### `/` (GET)
- **傳入**: 無
- **處理**: 預設頁面，無特殊邏輯
- **輸出**: 渲染 `index.html`

### `/draw` (POST)
- **傳入**: Session (判斷登入)
- **處理**: 呼叫 `Poem.get_all()` 並隨機選一個，若是註冊會員則建立 `Record.create()`
- **輸出**: 重導向至 `/result/<紀錄ID>`
- **錯誤**: 若抽籤失敗則返回首頁並顯示錯誤 flash

### `/result/<id>` (GET)
- **傳入**: URL 參數 `id`
- **處理**: `Record.get_by_id(id)` 返回紀錄及對應的 `Poem` 內容
- **輸出**: 渲染 `result.html`
- **錯誤**: 若查無紀錄則 404

### `/register` (GET / POST)
- **傳入**: 表單 `username`, `password`
- **處理**: GET 渲染，POST 驗證帳號是否重複，並將密碼加入 Hash 後 `User.create()`
- **輸出**: GET 渲染 `login.html`，POST 成功導向 `/login`
- **錯誤**: 帳號重複則 flash 失敗訊息，維持原頁面

### `/login` (GET / POST)
- **傳入**: 表單 `username`, `password`
- **處理**: GET 渲染，POST 核對資訊，建立 session
- **輸出**: GET 渲染 `login.html`，POST 成功導向 `/`
- **錯誤**: 帳號密碼錯誤則 flash 失敗訊息

### `/logout` (GET)
- **處理**: 清空 session
- **輸出**: 導向 `/`

### `/history` (GET)
- **處理**: 若未登入則導向登入頁；呼叫 `Record.get_all()` 過濾特定用戶
- **輸出**: 渲染 `history.html`

### `/donate` (GET / POST)
- **傳入**: 表單 `amount`, `message`
- **處理**: POST 若合法數字則 `Donation.create()`
- **輸出**: GET 渲染 `donate.html`，POST 成功 flash 訊息與重導向首頁

## 3. Jinja2 模板清單

所有的視圖檔皆繼承自 `base.html`：
- `base.html`: 包含共用的 Navbar (首頁, 捐香油錢, 登入/註冊, 我的紀錄) 與 Footer。
- `index.html`: 首頁與抽籤按鈕，並說明系統特色。
- `result.html`: 顯示抽出的籤詩及解籤說明，附帶分享按鈕。
- `history.html`: 單一會員專屬的抽籤紀錄表格。
- `login.html`: 藉由 flag 切換「登入」與「註冊」雙用途表單。
- `donate.html`: 輸入捐款金額、留言的模擬交易表單。

## 4. 路由骨架程式碼

路由的檔案位於 `app/routes/` 中，包含以下規劃：
- `main.py`: 主流程控制 (首頁, 抽籤, 結果, 捐香油錢)
- `auth.py`: 認證機制 (登入, 註冊, 登出)
- `history.py`: 使用者專屬歷史紀錄

