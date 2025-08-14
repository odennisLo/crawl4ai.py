#!/usr/bin/env python3
"""
Crawl4AI 基本測試範例
"""

import asyncio
from crawl4ai import AsyncWebCrawler

async def basic_crawl_test():
    """基本網頁爬取測試"""
    print("🚀 開始基本爬取測試...")
    
    async with AsyncWebCrawler() as crawler:
        # 測試爬取新聞網站
        print("📰 爬取新聞網站...")
        result = await crawler.arun(
            url="https://www.nbcnews.com/business",
        )
        
        print(f"✅ 爬取成功！")
        print(f"📄 頁面標題: {result.metadata.get('title', 'N/A')}")
        print(f"🔗 URL: {result.url}")
        print(f"📝 內容長度: {len(result.markdown)} 字元")
        print(f"🏷️ 提取到的連結數量: {len(result.links.get('external', [])) + len(result.links.get('internal', []))}")
        
        # 顯示部分內容
        if result.markdown:
            preview = result.markdown[:500] + "..." if len(result.markdown) > 500 else result.markdown
            print(f"\n📖 內容預覽:\n{preview}")

async def multiple_sites_test():
    """多個網站爬取測試"""
    print("\n🌐 開始多網站爬取測試...")
    
    urls = [
        "https://example.com",
        "https://httpbin.org/html",
        "https://quotes.toscrape.com"
    ]
    
    async with AsyncWebCrawler() as crawler:
        for i, url in enumerate(urls, 1):
            try:
                print(f"📍 ({i}/{len(urls)}) 爬取: {url}")
                result = await crawler.arun(url=url)
                print(f"   ✅ 成功 - 內容長度: {len(result.markdown)} 字元")
            except Exception as e:
                print(f"   ❌ 失敗: {str(e)}")

async def main():
    """主函數"""
    print("=" * 60)
    print("🕷️  Crawl4AI 測試程式")
    print("=" * 60)
    
    try:
        await basic_crawl_test()
        await multiple_sites_test()
        
        print("\n" + "=" * 60)
        print("🎉 所有測試完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
