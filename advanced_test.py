#!/usr/bin/env python3
"""
Crawl4AI 進階功能測試範例
"""

import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.extraction_strategy import CosineStrategy, LLMExtractionStrategy

async def structured_extraction_test():
    """結構化資料擷取測試"""
    print("🧠 開始結構化資料擷取測試...")
    
    async with AsyncWebCrawler() as crawler:
        # 使用 Cosine 策略擷取相似內容
        cosine_strategy = CosineStrategy(
            semantic_filter="technology news",
            word_count_threshold=10,
            max_dist=0.2,
            linkage_method='ward',
            top_k=3
        )
        
        result = await crawler.arun(
            url="https://news.ycombinator.com",
            extraction_strategy=cosine_strategy
        )
        
        print(f"✅ Cosine 策略擷取完成")
        print(f"📄 擷取到的內容塊數: {len(result.extracted_content) if result.extracted_content else 0}")
        
        if result.extracted_content:
            for i, content in enumerate(result.extracted_content[:3], 1):
                print(f"   📝 內容塊 {i}: {content[:100]}...")

async def javascript_execution_test():
    """JavaScript 執行測試"""
    print("\n⚡ 開始 JavaScript 執行測試...")
    
    js_code = """
    // 獲取頁面基本資訊
    const info = {
        title: document.title,
        url: window.location.href,
        userAgent: navigator.userAgent,
        timestamp: new Date().toISOString(),
        links: Array.from(document.links).slice(0, 5).map(link => ({
            text: link.textContent.trim(),
            href: link.href
        }))
    };
    info;
    """
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://example.com",
            js_code=js_code
        )
        
        print(f"✅ JavaScript 執行完成")
        if result.js_execution_result:
            print(f"📊 執行結果: {json.dumps(result.js_execution_result, indent=2, ensure_ascii=False)}")

async def css_selector_test():
    """CSS 選擇器測試"""
    print("\n🎯 開始 CSS 選擇器測試...")
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://quotes.toscrape.com",
            css_selector="div.quote"  # 選擇引用區塊
        )
        
        print(f"✅ CSS 選擇器擷取完成")
        print(f"📝 擷取到的內容長度: {len(result.markdown)} 字元")
        if result.markdown:
            preview = result.markdown[:300] + "..." if len(result.markdown) > 300 else result.markdown
            print(f"📖 內容預覽:\n{preview}")

async def screenshot_test():
    """螢幕截圖測試"""
    print("\n📸 開始螢幕截圖測試...")
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://example.com",
            screenshot=True
        )
        
        print(f"✅ 螢幕截圖完成")
        if result.screenshot:
            # 儲存截圖
            with open("/Users/dennis.lo/crawl4ai.py/screenshot.png", "wb") as f:
                f.write(result.screenshot)
            print(f"💾 截圖已儲存至: screenshot.png")

async def user_agent_test():
    """自訂 User Agent 測試"""
    print("\n🤖 開始自訂 User Agent 測試...")
    
    custom_config = CrawlerRunConfig(
        user_agent="Crawl4AI-Test-Bot/1.0"
    )
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://httpbin.org/user-agent",
            config=custom_config
        )
        
        print(f"✅ User Agent 測試完成")
        print(f"📄 回應內容: {result.markdown}")

async def main():
    """主函數"""
    print("=" * 60)
    print("🚀 Crawl4AI 進階功能測試程式")
    print("=" * 60)
    
    try:
        await structured_extraction_test()
        await javascript_execution_test()
        await css_selector_test()
        await screenshot_test()
        await user_agent_test()
        
        print("\n" + "=" * 60)
        print("🎉 所有進階測試完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
