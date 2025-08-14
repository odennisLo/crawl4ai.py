#!/usr/bin/env python3
"""
台灣網站爬取範例
"""

import asyncio
import json
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def taiwan_news_test():
    """台灣新聞網站測試"""
    print("🇹🇼 開始台灣新聞網站測試...")
    
    taiwan_news_sites = [
        ("中央社", "https://www.cna.com.tw"),
        ("自由時報", "https://www.ltn.com.tw"),
        ("聯合新聞網", "https://udn.com"),
    ]
    
    async with AsyncWebCrawler() as crawler:
        for name, url in taiwan_news_sites:
            try:
                print(f"📰 正在爬取 {name}: {url}")
                result = await crawler.arun(url=url)
                
                print(f"   ✅ {name} 爬取成功")
                print(f"   📄 標題: {result.metadata.get('title', 'N/A')}")
                print(f"   📝 內容長度: {len(result.markdown)} 字元")
                print(f"   🔗 連結數量: {len(result.links.get('internal', [])) + len(result.links.get('external', []))}")
                
                # 顯示部分內容
                if result.markdown:
                    preview = result.markdown[:200] + "..." if len(result.markdown) > 200 else result.markdown
                    print(f"   📖 內容預覽: {preview}")
                print()
                
            except Exception as e:
                print(f"   ❌ {name} 爬取失敗: {str(e)}")
                print()

async def ptt_test():
    """PTT 網站測試"""
    print("💬 開始 PTT 網站測試...")
    
    async with AsyncWebCrawler() as crawler:
        try:
            print("📍 正在爬取 PTT 首頁...")
            result = await crawler.arun(url="https://www.ptt.cc/bbs/index.html")
            
            print(f"✅ PTT 爬取成功")
            print(f"📄 標題: {result.metadata.get('title', 'N/A')}")
            print(f"📝 內容長度: {len(result.markdown)} 字元")
            
            if result.markdown:
                preview = result.markdown[:300] + "..." if len(result.markdown) > 300 else result.markdown
                print(f"📖 內容預覽:\n{preview}")
                
        except Exception as e:
            print(f"❌ PTT 爬取失敗: {str(e)}")

async def government_site_test():
    """政府網站測試"""
    print("\n🏛️ 開始政府網站測試...")
    
    gov_sites = [
        ("總統府", "https://www.president.gov.tw"),
        ("行政院", "https://www.ey.gov.tw"),
        ("數位發展部", "https://www.moda.gov.tw"),
    ]
    
    async with AsyncWebCrawler() as crawler:
        for name, url in gov_sites:
            try:
                print(f"🏛️ 正在爬取 {name}: {url}")
                result = await crawler.arun(url=url)
                
                print(f"   ✅ {name} 爬取成功")
                print(f"   📄 標題: {result.metadata.get('title', 'N/A')}")
                print(f"   📝 內容長度: {len(result.markdown)} 字元")
                print()
                
            except Exception as e:
                print(f"   ❌ {name} 爬取失敗: {str(e)}")
                print()

async def ecommerce_test():
    """電商網站測試"""
    print("🛒 開始電商網站測試...")
    
    ecommerce_sites = [
        ("PChome", "https://www.pchome.com.tw"),
        ("momo購物網", "https://www.momoshop.com.tw"),
    ]
    
    async with AsyncWebCrawler() as crawler:
        for name, url in ecommerce_sites:
            try:
                print(f"🛒 正在爬取 {name}: {url}")
                result = await crawler.arun(url=url)
                
                print(f"   ✅ {name} 爬取成功")
                print(f"   📄 標題: {result.metadata.get('title', 'N/A')}")
                print(f"   📝 內容長度: {len(result.markdown)} 字元")
                print()
                
            except Exception as e:
                print(f"   ❌ {name} 爬取失敗: {str(e)}")
                print()

async def tech_blog_test():
    """科技部落格測試"""
    print("💻 開始科技部落格測試...")
    
    tech_blogs = [
        ("iThome", "https://www.ithome.com.tw"),
        ("科技新報", "https://technews.tw"),
    ]
    
    async with AsyncWebCrawler() as crawler:
        for name, url in tech_blogs:
            try:
                print(f"💻 正在爬取 {name}: {url}")
                result = await crawler.arun(url=url)
                
                print(f"   ✅ {name} 爬取成功")
                print(f"   📄 標題: {result.metadata.get('title', 'N/A')}")
                print(f"   📝 內容長度: {len(result.markdown)} 字元")
                print()
                
            except Exception as e:
                print(f"   ❌ {name} 爬取失敗: {str(e)}")
                print()

async def main():
    """主函數"""
    print("=" * 60)
    print("🇹🇼 台灣網站爬取測試程式")
    print("=" * 60)
    
    try:
        await taiwan_news_test()
        await ptt_test()
        await government_site_test()
        await ecommerce_test()
        await tech_blog_test()
        
        print("=" * 60)
        print("🎉 所有台灣網站測試完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
