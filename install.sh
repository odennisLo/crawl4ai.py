#!/bin/bash

echo "🚀 Crawl4AI 專案安裝腳本"
echo "=========================="

# 檢查 Python 版本
python_version=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+')
echo "✅ 檢測到 Python 版本: $python_version"

# 建立虛擬環境
echo "📦 建立虛擬環境..."
python3 -m venv .venv

# 啟動虛擬環境
echo "🔄 啟動虛擬環境..."
source .venv/bin/activate

# 升級 pip
echo "⬆️ 升級 pip..."
pip install --upgrade pip

# 安裝套件
echo "📚 安裝套件..."
pip install -r requirements.txt

# 執行 Crawl4AI 設定
echo "⚙️ 執行 Crawl4AI 安裝後設定..."
crawl4ai-setup

# 健康檢查
echo "🔍 執行健康檢查..."
python -c "from crawl4ai import *; print('✅ Crawl4AI 安裝成功！')"

echo ""
echo "🎉 安裝完成！"
echo ""
echo "使用方法："
echo "1. 啟動虛擬環境: source .venv/bin/activate"
echo "2. 執行測試: python esports_test.py"
echo ""
