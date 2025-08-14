# Crawl4AI Python 測試專案

這是一個使用 [Crawl4AI](https://github.com/unclecode/crawl4ai) 套件的 Python 測試專案。Crawl4AI 是一個開源的、對 LLM 友善的網頁爬蟲和抓取工具。

## �️ 環境設定

### 1. 建立虛擬環境
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. 安裝套件
```bash
pip install -r requirements.txt
```

### 3. 安裝後設定（重要！）
```bash
crawl4ai-setup
```

### 4. 健康檢查
```bash
python -c "from crawl4ai import *; print('✅ Crawl4AI 安裝成功！')"
```

## 🚀 快速開始

### 執行測試腳本
```bash
# 基本功能測試
python basic_test.py

# 進階功能測試
python advanced_test.py

# CLI 測試
python cli_test.py

# 台灣網站測試
python taiwan_sites_test.py

# 電競新聞測試（含圖片下載）
python esports_test.py
```

## 📁 專案結構

```
crawl4ai.py/
├── 🐍 Python 腳本
│   ├── basic_test.py         # 基本功能測試
│   ├── advanced_test.py      # 進階功能測試
│   ├── cli_test.py           # CLI 命令列測試
│   ├── taiwan_sites_test.py  # 台灣網站測試
│   ├── esports_test.py       # 電競新聞網站測試（含圖片下載）
│   └── esports_debug.py      # 電競網站除錯腳本
├── 📋 設定檔案
│   ├── requirements.txt      # Python 套件清單
│   ├── README.md            # 專案說明
│   └── .gitignore           # Git 忽略檔案清單
├── 🛠️ 工具腳本
│   ├── install.sh           # 自動安裝腳本
│   └── clean.sh             # 清理腳本
└── 🚫 排除檔案（.gitignore）
    ├── .venv/              # Python 虛擬環境
    ├── *_images_*/         # 測試產生的圖片資料夾
    ├── *.json              # 測試結果檔案
    └── *.png               # 截圖檔案
```

## 📋 套件需求

主要套件：
- `crawl4ai==0.7.3` - 主要爬蟲套件
- `aiohttp` - 非同步 HTTP 客戶端（用於圖片下載）
- `aiofiles` - 非同步檔案操作（用於圖片儲存）

完整清單請參考 `requirements.txt`

## 🧪 測試內容

### basic_test.py - 基本功能測試
- ✅ 基本網頁爬取
- ✅ 多個網站爬取
- ✅ 內容長度和連結統計
- ✅ 結果預覽

### advanced_test.py - 進階功能測試
- 🧠 結構化資料擷取 (Cosine Strategy)
- ⚡ JavaScript 執行
- 🎯 CSS 選擇器
- 📸 螢幕截圖
- 🤖 自訂 User Agent

### cli_test.py - CLI 測試
- 📋 JSON 格式擷取
- ✂️ 正規表達式分塊
- 🔗 連結分析
- 📊 元資料擷取
- ⚡ 效能測試

### esports_test.py - 電競新聞測試
- 🎮 電競新聞文章擷取
- 🖼️ 圖片擷取和分析
- 📸 網頁截圖
- 🎯 CSS 選擇器測試
- ⚙️ 自訂爬蟲配置
- 📁 自動圖片下載（資料夾命名：測試名稱_images_時間戳記）
- 📊 下載統計報告

## ⚠️ 重要注意事項

### 首次安裝
1. **必須執行安裝後設定**：`crawl4ai-setup`
2. **系統需求**：需要 Python 3.8+ 和足夠的磁碟空間
3. **網路連線**：需要穩定的網路連線下載瀏覽器元件

### 使用限制
- 圖片下載會跳過 SSL 證書驗證（針對某些網站的相容性）
- 併發下載限制為 5 個同時連線（避免伺服器負載）
- 某些網站可能會回傳 404 錯誤（這是正常的）

### 版本控制
- `.venv/` 資料夾已加入 `.gitignore`，不會包含在版本控制中
- 測試產生的圖片資料夾和結果檔案也會被忽略
- 其他開發者需要重新建立虛擬環境和安裝套件

## 🎯 給其他開發者

### 方法 1：自動安裝（推薦）
```bash
# 下載專案後執行
./install.sh
```

### 方法 2：手動安裝
如果您是第一次使用這個專案：

1. **下載專案**（不包含 .venv）
2. **建立虛擬環境**：`python3 -m venv .venv`
3. **啟動環境**：`source .venv/bin/activate`
4. **安裝套件**：`pip install -r requirements.txt`
5. **重要設定**：`crawl4ai-setup`
6. **開始測試**：`python esports_test.py`

### 清理測試檔案
```bash
# 清理所有測試產生的檔案和圖片
./clean.sh
```

## 📂 專案分享

當您要分享這個專案給其他人時：

✅ **包含的檔案**：
- 所有 `.py` 腳本
- `requirements.txt`
- `README.md`
- `.gitignore`
- `install.sh` 和 `clean.sh`

❌ **排除的檔案**（自動忽略）：
- `.venv/` 虛擬環境
- `*_images_*/` 圖片資料夾
- `*.json` 結果檔案
- `*.png` 截圖檔案
- `__pycache__/` Python 快取

## 🛠️ 主要功能

### 基本爬取
```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def basic_crawl():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url="https://example.com")
        print(result.markdown)

asyncio.run(basic_crawl())
```

### 結構化資料擷取
```python
from crawl4ai.extraction_strategy import CosineStrategy

cosine_strategy = CosineStrategy(
    semantic_filter="technology news",
    word_count_threshold=10,
    max_dist=0.2,
    top_k=3
)

result = await crawler.arun(
    url="https://news.ycombinator.com",
    extraction_strategy=cosine_strategy
)
```

### JavaScript 執行
```python
js_code = """
const info = {
    title: document.title,
    url: window.location.href,
    timestamp: new Date().toISOString()
};
info;
"""

result = await crawler.arun(
    url="https://example.com",
    js_code=js_code
)
```

### CSS 選擇器
```python
result = await crawler.arun(
    url="https://quotes.toscrape.com",
    css_selector="div.quote"
)
```

## 📋 命令列工具

Crawl4AI 也提供了強大的命令列工具：

```bash
# 基本爬取並輸出 Markdown
crwl https://www.nbcnews.com/business -o markdown

# 深度爬取，最多 10 頁
crwl https://docs.crawl4ai.com --deep-crawl bfs --max-pages 10

# 使用 LLM 擷取特定問題的答案
crwl https://www.example.com/products -q "Extract all product prices"
```

## 🔧 安裝後設置

如果你重新安裝或遇到問題，可以運行：

```bash
# 重新設置 Crawl4AI
crawl4ai-setup

# 檢查安裝狀態
crawl4ai-doctor
```

## 📖 更多資源

- [官方文件](https://docs.crawl4ai.com/)
- [GitHub 倉庫](https://github.com/unclecode/crawl4ai)
- [範例程式](https://github.com/unclecode/crawl4ai/tree/main/docs/examples)
- [Google Colab 範例](https://colab.research.google.com/drive/1SgRPrByQLzjRfwoRNq1wSGE9nYY_EE8C?usp=sharing)

## 🆘 故障排除

如果遇到瀏覽器相關問題，可以手動安裝：

```bash
python -m playwright install --with-deps chromium
```

## 📝 注意事項

- 確保網路連接正常
- 某些網站可能有反爬蟲機制
- 大型網站爬取可能需要較長時間
- 尊重網站的 robots.txt 和使用條款

## 🎯 下一步

1. 嘗試爬取不同類型的網站
2. 實驗不同的擷取策略
3. 結合 LLM 進行內容分析
4. 建立自己的爬蟲應用程式

祝爬蟲愉快！🕷️🚀
