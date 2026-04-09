# 流程圖設計 - 線上算命系統

根據產品需求與系統架構設計，本文件將系統操作與資料流視覺化，確保開發團隊對使用者行為的想像一致，並定義出未來將開發的 Web 路由。

---

## 1. 使用者流程圖（User Flow）
此圖描繪了使用者從進入網站開始，可能進入的頁面以及進行的各種操作流程。

```mermaid
flowchart LR
    A([訪客進入網站]) --> B[首頁 - 抽籤與介紹]
    B --> C{是否已登入？}
    
    C -->|否| D[進行一般抽籤/占卜]
    D --> E[查看抽籤結果]
    E --> F[分享結果到社群]
    E --> G[點擊登入以便紀錄未來籤詩]
    G --> H[註冊/登入頁面]
    
    C -->|是| I[進行登入狀態抽籤]
    I --> J[查看並自動儲存結果]
    J --> F
    
    H -->|成功| B
    B --> K[歷史紀錄頁面]
    K --> L[檢視過去抽籤紀錄與詳細解籤]
    
    B --> M[捐獻香油錢頁面]
    M --> N[填寫捐獻金額與祈福資訊]
    N --> O[完成模擬捐款並感謝]
```

---

## 2. 系統序列圖（Sequence Diagram）
此圖以「使用者進行一次抽籤並儲存」作為範例，描述系統底層前端、控制器與資料庫如何互動並傳遞訊息。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask (routes.py)
    participant Model as Model (models.py)
    participant DB as SQLite 資料庫

    User->>Browser: 點選「開始抽籤」按鈕
    Browser->>Route: POST /draw (夾帶 Cookie/Session 確認登入)
    Route->>Route: 亂數或邏輯運算得出籤詩編號
    
    rect rgb(230, 240, 255)
        Note right of Route: 會員的資料庫寫入階段
        Route->>Model: 建立 UserRecord 物件 (User ID, 籤詩編號)
        Model->>DB: INSERT INTO records
        DB-->>Model: 寫入成功
        Model-->>Route: 取得該次寫入的紀錄 ID
    end
    
    Route-->>Browser: 重導向 (Redirect) 到 /result/<紀錄ID>
    Browser->>Route: GET /result/<紀錄ID>
    Route->>Model: 查詢特定抽籤紀錄
    Model->>DB: SELECT * FROM records WHERE id = ?
    DB-->>Model: 回傳所求的紀錄 (含籤詩內容)
    Model-->>Route: 轉換為物件
    Route->>Route: 將資料餵進 Jinja2 模板 (result.html)
    Route-->>Browser: 回傳完整的 HTML 畫面
    Browser-->>User: 顯示抽籤結果與解籤資訊
```

---

## 3. 功能清單與路由對照表
整理出主要的頁面與操作，對應未來要實作的 Flask 路由。系統設計符合基本的 REST 風格與表單提交習慣：

| 頁面/功能項目 | HTTP 方法 | URL 路徑 | 功能說明 |
| :--- | :--- | :--- | :--- |
| **首頁與操作入口** | GET | `/` | 介紹系統，並提供開始抽籤的按鈕。 |
| **執行抽籤邏輯** | POST | `/draw` | 負責亂數產生結果、若已登入則寫入資料庫，隨後跳轉。 |
| **檢視單次結果** | GET | `/result/<id>` | 抽籤後展示籤詩與解開的內容，此連結可用來網頁分享。 |
| **註冊頁面** | GET | `/register` | 填寫會員註冊用的表單。 |
| **註冊送出** | POST | `/register` | 接收表單並將新會員存入資料庫。 |
| **登入頁面** | GET | `/login` | 填寫會員登入資訊。 |
| **登入送出** | POST | `/login` | 核對帳號密碼，成功則建立 Session。 |
| **登出** | GET | `/logout` | 清除登入 Session 狀態並導回首頁。 |
| **歷史紀錄列表** | GET | `/history` | (需登入) 從資料庫撈出該會員過往求得的所有籤詩。 |
| **香油錢捐獻頁面** | GET | `/donate` | 顯示捐款表單與模擬付款介紹。 |
| **送出模擬捐獻** | POST | `/donate` | 接收捐款意向，寫入 Donation 資料表作為紀錄。 |
