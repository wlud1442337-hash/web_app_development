# 系統架構設計 - 線上算命系統

## 1. 技術架構說明

本系統為一款提供線上算命、占卜與抽籤體驗的 Web 應用程式。為了達到快速開發並驗證市場的目標，我們選擇了輕量而強大的技術組合。

### 選用技術與原因
- **後端框架：Python + Flask**
  Flask 是輕量級的微框架，彈性極高，不用綁定複雜的套件，非常適合用來快速打造本專案的 API 與網頁路由。
- **模板引擎：Jinja2**
  在本專案中不需要複雜的前後端分離框架（如 React/Vue）。Jinja2 與 Flask 深度整合，讓我們能夠在伺服器端將資料直接渲染成 HTML，減少前後端 API 溝通的開發成本，同時有良好的 SEO 支援。
- **資料庫：SQLite**
  SQLite 輕巧且免安裝額外伺服器。透過檔案形式儲存，非常適合 MVP 階段、開發與測試環境。

### Flask MVC 模式說明
開發將遵循 MVC (Model-View-Controller) 架構模式的變體：
- **Model (模型)**：負責商業邏輯與資料定義。如定義使用者 (User)、算命紀錄 (Record)、香油錢捐獻 (Donation) 這些資料表格式。
- **View (視圖)**：負責畫面的展示。即我們系統裡的 Jinja2 模板檔 (.html) 與靜態檔 (CSS/JS)，決定使用者最終看到的算命畫面與按鈕。
- **Controller (控制器)**：負責接發請求與控制流程。即 Flask 的路由 (Routes)。它會接收使用者的動作（如點擊「抽籤」），向 Model 取出相對應的籤詩資料，最後交由 View 負責渲染出給使用者看的結果頁面。

---

## 2. 專案資料夾結構

本專案採用典型的 Flask 模組化結構，方便元件的拆分與未來擴展：

```text
web_app_development/
├── app/                  # 應用程式主目錄
│   ├── __init__.py       # 初始化 Flask 實體、載入配置、初始化資料庫套件
│   ├── models.py         # 資料庫模型結構 (User, Record, Donation)
│   ├── routes.py         # 所有的 HTTP 路由與端點 (Controller)
│   ├── templates/        # Jinja2 HTML 模板檔 (View)
│   │   ├── base.html     # 基本共用母版 (包含 Navbar與 Footer)
│   │   ├── index.html    # 首頁 / 主要的抽籤占卜頁面
│   │   ├── history.html  # 歷史算命紀錄列表頁面
│   │   ├── login.html    # 登入與註冊頁面
│   │   └── donate.html   # 香油錢捐獻頁面
│   └── static/           # 前端靜態資源
│       ├── css/          # 樣式表 (style.css)
│       ├── js/           # 客製化互動指令碼 (如抽籤罐搖晃動畫)
│       └── images/       # 各式圖片 (籤詩圖、背景圖等)
├── instance/             # 存放執行期產生的機密或本地資料
│   └── database.db       # SQLite 資料庫檔案
├── docs/                 # 專案說明文件 (如 PRD.md, ARCHITECTURE.md)
├── config.py             # 環境與系統設定檔 (如資料庫路徑、Session Key)
├── requirements.txt      # Python 相依套件清單
└── app.py                # 應用程式進入點，負責啟動伺服器
```

---

## 3. 元件關係圖

以下展示了系統在收到使用者請求時，元件之間互動的流程：

```mermaid
flowchart TD
    Browser[使用者 / 瀏覽器] -->|1. 發出 HTTP Request (如點擊抽籤)| Routes([Flask Routes / 控制器])
    
    Routes -->|2. 讀寫 / 查詢| Models([Models / 資料模型])
    Models <-->|3. 執行 SQL 語法| SQLite[(SQLite 資料庫)]
    
    Models -->|4. 回傳實體資料| Routes
    Routes -->|5. 餵入資料| Templates([Jinja2 Templates / 模板])
    
    Templates -->|6. 渲染為 HTML 結構| Routes
    Routes -->|7. 回傳 HTTP Response| Browser
```

---

## 4. 關鍵設計決策

1. **伺服器端渲染 (SSR)**  
   **決策**：決定採用 Flask + Jinja2 而非 前後端分離 (API + React)。  
   **原因**：系統焦點在於簡單的操作流程與內容展示。SSR 能加快整體專案的建置速度，並且更容易幫助爬蟲抓取分享頁面的中繼資料（用於社群分享的需求）。

2. **內建 SQLite 作為 MVP 資料庫**  
   **決策**：不架設獨立的 MySQL 或 PostgreSQL，而是直接使用本地端的資料庫檔案。  
   **原因**：線上算命系統初期通常重讀（抽籤查詢）輕寫（會員註冊或歷史儲存），SQLite 完全能從容應對這樣的 I/O 負載，也大幅降低了初期的部署難度與成本。

3. **抽籤邏輯由後端全權控制**  
   **決策**：抽籤或占卜的隨機過程與資料庫存取，必須在後端伺服器 (Flask Route) 處理，而不是將所有籤詩資料吐給前端進行隨機。  
   **原因**：避免前端程式碼被直接解析而看透所有籤詩，同時將結果強制紀錄到後端能確保「儲存抽籤結果」之功能的一致性。

4. **模擬金流設計**  
   **決策**：「捐香油錢」將暫無涉入真實第三方支付平台的串接，而是將此行為製作為流程模擬，並紀錄狀態進入資料庫。  
   **原因**：避免在專案早期耗費龐大的時間申請 API 密鑰審核與測試沙盒，優先將人力放在核心業務 (抽籤/登入)。我們預留了 `Donation` 模型以便未來無縫切換為串接真實金流。
