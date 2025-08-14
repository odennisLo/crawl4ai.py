#!/bin/bash
# Crawl4AI 專案快速設置腳本

echo "🚀 Crawl4AI 專案快速設置"
echo "========================"

# 檢查是否在正確的目錄
if [ ! -f "README.md" ] || [ ! -d ".venv" ]; then
    echo "❌ 請在 crawl4ai.py 專案目錄中執行此腳本"
    exit 1
fi

# 啟動虛擬環境
echo "📦 啟動虛擬環境..."
source .venv/bin/activate

# 檢查 Crawl4AI 安裝
echo "🔍 檢查 Crawl4AI 安裝狀態..."
if ! command -v crawl4ai-doctor &> /dev/null; then
    echo "❌ Crawl4AI 未正確安裝"
    echo "🔧 正在重新安裝..."
    pip install crawl4ai
    crawl4ai-setup
fi

# 運行健康檢查
echo "🏥 運行健康檢查..."
crawl4ai-doctor

echo ""
echo "✅ 設置完成！"
echo ""
echo "🎯 可用的命令："
echo "   python run_tests.py     # 啟動測試選單"
echo "   python basic_test.py    # 基本功能測試"
echo "   python advanced_test.py # 進階功能測試"
echo "   python cli_test.py      # CLI 測試"
echo "   python taiwan_sites_test.py # 台灣網站測試"
echo ""
echo "📚 查看說明： cat README.md"
echo ""
echo "🚀 開始使用吧！"
