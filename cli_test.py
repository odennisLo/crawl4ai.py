#!/usr/bin/env python3
"""
Crawl4AI CLI 命令列測試範例
"""

import asyncio
import json
from crawl4ai import AsyncWebCrawler
from crawl4ai.chunking_strategy import RegexChunking
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def json_extraction_test():
    """JSON 格式擷取測試"""
    print("📋 開始 JSON 擷取測試...")
    
    # 定義要擷取的資料結構
    schema = {
        "name": "新聞文章",
        "baseSelector": "article, .article, .post",
        "fields": [
            {
                "name": "title",
                "selector": "h1, h2, .title",
                "type": "text"
            },
            {
                "name": "content", 
                "selector": "p, .content",
                "type": "text"
            },
            {
                "name": "author",
                "selector": ".author, .by-author",
                "type": "text"
            },
            {
                "name": "date",
                "selector": ".date, .published",
                "type": "text"
            }
        ]
    }
    
    extraction_strategy = JsonCssExtractionStrategy(schema)
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://news.ycombinator.com",
            extraction_strategy=extraction_strategy
        )
        
        print(f"✅ JSON 擷取完成")
        if result.extracted_content:
            try:
                data = json.loads(result.extracted_content)
                print(f"📊 擷取到 {len(data)} 筆資料")
                if data:
                    print(f"📝 第一筆資料範例:")
                    print(json.dumps(data[0], indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print(f"📄 原始擷取內容: {result.extracted_content[:500]}...")

async def regex_chunking_test():
    """正規表達式分塊測試"""
    print("\n✂️ 開始正規表達式分塊測試...")
    
    # 使用標題來分塊內容
    chunking_strategy = RegexChunking(
        patterns=[r'\n#{1,6}\s+(.+)', r'\n\*\*(.+?)\*\*']
    )
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://docs.python.org/3/tutorial/",
            chunking_strategy=chunking_strategy
        )
        
        print(f"✅ 分塊完成")
        if hasattr(result, 'chunks') and result.chunks:
            print(f"📦 分塊數量: {len(result.chunks)}")
            for i, chunk in enumerate(result.chunks[:3], 1):
                preview = chunk[:100] + "..." if len(chunk) > 100 else chunk
                print(f"   📝 塊 {i}: {preview}")

async def links_analysis_test():
    """連結分析測試"""
    print("\n🔗 開始連結分析測試...")
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://github.com/unclecode/crawl4ai"
        )
        
        print(f"✅ 連結分析完成")
        
        if result.links:
            internal_links = result.links.get('internal', [])
            external_links = result.links.get('external', [])
            
            print(f"🏠 內部連結數量: {len(internal_links)}")
            print(f"🌐 外部連結數量: {len(external_links)}")
            
            if internal_links:
                print(f"📋 前5個內部連結:")
                for i, link in enumerate(internal_links[:5], 1):
                    print(f"   {i}. {link}")
            
            if external_links:
                print(f"📋 前5個外部連結:")
                for i, link in enumerate(external_links[:5], 1):
                    print(f"   {i}. {link}")

async def metadata_extraction_test():
    """元資料擷取測試"""
    print("\n📊 開始元資料擷取測試...")
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://www.python.org"
        )
        
        print(f"✅ 元資料擷取完成")
        
        if result.metadata:
            print(f"📋 元資料:")
            for key, value in result.metadata.items():
                if isinstance(value, str) and len(value) > 100:
                    value = value[:100] + "..."
                print(f"   {key}: {value}")

async def performance_test():
    """效能測試"""
    print("\n⚡ 開始效能測試...")
    
    import time
    
    urls = [
        "https://example.com",
        "https://httpbin.org/html",
        "https://quotes.toscrape.com"
    ]
    
    start_time = time.time()
    
    async with AsyncWebCrawler() as crawler:
        for url in urls:
            single_start = time.time()
            result = await crawler.arun(url=url)
            single_time = time.time() - single_start
            print(f"   📍 {url}: {single_time:.2f}s (內容: {len(result.markdown)} 字元)")
    
    total_time = time.time() - start_time
    print(f"⏱️ 總執行時間: {total_time:.2f}s")
    print(f"📈 平均每個URL: {total_time/len(urls):.2f}s")

async def main():
    """主函數"""
    print("=" * 60)
    print("🧪 Crawl4AI CLI 測試程式")
    print("=" * 60)
    
    try:
        await json_extraction_test()
        await regex_chunking_test()
        await links_analysis_test()
        await metadata_extraction_test()
        await performance_test()
        
        print("\n" + "=" * 60)
        print("🎉 所有 CLI 測試完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
