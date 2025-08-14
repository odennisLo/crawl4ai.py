#!/usr/bin/env python3
"""
Crawl4AI 測試選單
"""

import os
import sys
import subprocess

def run_script(script_name):
    """執行指定的腳本"""
    try:
        # 確保在正確的目錄中（使用相對路徑）
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # 啟動虛擬環境並執行腳本
        cmd = f"source .venv/bin/activate && python {script_name}"
        subprocess.run(cmd, shell=True, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 執行 {script_name} 時發生錯誤: {e}")
    except Exception as e:
        print(f"❌ 發生未預期的錯誤: {e}")

def show_menu():
    """顯示選單"""
    print("=" * 60)
    print("🕷️  Crawl4AI 測試選單")
    print("=" * 60)
    print()
    print("請選擇要執行的測試:")
    print("1. 基本功能測試 (basic_test.py)")
    print("2. 進階功能測試 (advanced_test.py)")
    print("3. CLI 測試 (cli_test.py)")
    print("4. 台灣網站測試 (taiwan_sites_test.py)")
    print("5. 電競新聞測試 (esports_test.py)")
    print("6. 查看專案說明 (README.md)")
    print("7. 安裝後檢查 (crawl4ai-doctor)")
    print("0. 結束程式")
    print()

def main():
    """主函數"""
    while True:
        show_menu()
        
        try:
            choice = input("請輸入選項 (0-7): ").strip()
            
            if choice == "0":
                print("👋 再見！")
                break
            elif choice == "1":
                print("🚀 執行基本功能測試...")
                run_script("basic_test.py")
            elif choice == "2":
                print("🧪 執行進階功能測試...")
                run_script("advanced_test.py")
            elif choice == "3":
                print("📋 執行 CLI 測試...")
                run_script("cli_test.py")
            elif choice == "4":
                print("🇹🇼 執行台灣網站測試...")
                run_script("taiwan_sites_test.py")
            elif choice == "5":
                print("🎮 執行電競新聞測試...")
                run_script("esports_test.py")
            elif choice == "6":
                print("📖 顯示專案說明...")
                try:
                    with open("README.md", "r", encoding="utf-8") as f:
                        content = f.read()
                        print("\n" + content)
                except FileNotFoundError:
                    print("❌ 找不到 README.md 檔案")
            elif choice == "7":
                print("🔍 執行安裝後檢查...")
                try:
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    os.chdir(script_dir)
                    cmd = "source .venv/bin/activate && crawl4ai-doctor"
                    subprocess.run(cmd, shell=True, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"❌ 執行檢查時發生錯誤: {e}")
            else:
                print("❌ 無效的選項，請重新選擇")
            
            if choice != "0":
                input("\n按 Enter 鍵繼續...")
                print("\n" * 2)  # 清空畫面
                
        except KeyboardInterrupt:
            print("\n👋 再見！")
            break
        except Exception as e:
            print(f"❌ 發生錯誤: {e}")
            input("\n按 Enter 鍵繼續...")

if __name__ == "__main__":
    main()
