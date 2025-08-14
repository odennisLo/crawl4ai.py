#!/bin/bash

echo "🧹 清理專案檔案"
echo "==============="

# 清理測試產生的檔案
echo "🗑️ 清理測試結果檔案..."
rm -f *.json
rm -f *.png

# 清理圖片資料夾
echo "🖼️ 清理圖片資料夾..."
rm -rf *_images_*/

# 清理 Python 快取
echo "🐍 清理 Python 快取..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# 清理 .DS_Store 檔案 (macOS)
echo "🍎 清理 macOS 系統檔案..."
find . -name ".DS_Store" -delete 2>/dev/null || true

echo "✅ 清理完成！"
echo ""
echo "保留的檔案："
echo "- 所有 Python 腳本 (.py)"
echo "- requirements.txt"
echo "- README.md"
echo "- .gitignore"
echo "- .venv/ (如果存在)"
echo ""
