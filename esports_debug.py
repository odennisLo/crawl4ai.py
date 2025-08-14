#!/usr/bin/env python3
"""
專門針對 esports.net 圖片擷取的詳細測試
"""

import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig

async def debug_image_extraction():
    """詳細的圖片擷取除錯測試"""
    print("🔍 開始詳細圖片擷取除錯...")
    
    url = "https://www.esports.net/news/counter-strike/cs2-roster-shake-up-heroic-benches-gr1ks-fut-signs-ex-navi-juniors-with-misutaaa/"
    
    # 詳細的除錯 JavaScript
    debug_js = """
    console.log('開始圖片除錯...');
    
    // 等待頁面完全載入
    await new Promise(resolve => {
        if (document.readyState === 'complete') {
            console.log('頁面已完全載入');
            resolve();
        } else {
            console.log('等待頁面載入...');
            window.addEventListener('load', () => {
                console.log('頁面載入完成');
                resolve();
            });
        }
    });
    
    // 額外等待時間
    await new Promise(resolve => setTimeout(resolve, 3000));
    console.log('等待完成，開始分析圖片...');
    
    // 1. 基本圖片統計
    const allImages = document.querySelectorAll('img');
    console.log(`找到 ${allImages.length} 個 img 元素`);
    
    // 2. 分析每個圖片
    const imageDetails = [];
    allImages.forEach((img, index) => {
        const detail = {
            index: index + 1,
            tagName: img.tagName,
            src: img.src || 'NO_SRC',
            alt: img.alt || 'NO_ALT',
            className: img.className || 'NO_CLASS',
            id: img.id || 'NO_ID',
            width: img.width || 'NO_WIDTH',
            height: img.height || 'NO_HEIGHT',
            naturalWidth: img.naturalWidth || 'NO_NATURAL_WIDTH',
            naturalHeight: img.naturalHeight || 'NO_NATURAL_HEIGHT',
            srcset: img.srcset || 'NO_SRCSET',
            loading: img.loading || 'NO_LOADING',
            complete: img.complete,
            parentElement: img.parentElement ? img.parentElement.tagName : 'NO_PARENT',
            parentClass: img.parentElement ? img.parentElement.className : 'NO_PARENT_CLASS'
        };
        
        imageDetails.push(detail);
        console.log(`圖片 ${index + 1}: ${detail.src.substring(0, 50)}...`);
    });
    
    // 3. 查找 WordPress 圖片容器
    const wpCaptions = document.querySelectorAll('.wp-caption, [class*="wp-caption"]');
    console.log(`找到 ${wpCaptions.length} 個 WordPress 圖片容器`);
    
    const wpImages = [];
    wpCaptions.forEach((caption, index) => {
        const img = caption.querySelector('img');
        if (img) {
            wpImages.push({
                containerIndex: index + 1,
                containerClass: caption.className,
                containerId: caption.id || 'NO_ID',
                imgSrc: img.src,
                imgAlt: img.alt,
                imgSrcset: img.srcset || 'NO_SRCSET'
            });
        }
    });
    
    // 4. 查找文章內容區域
    const articleContent = document.querySelector('article, .article-content, .post-content, .entry-content, main');
    let contentImages = [];
    if (articleContent) {
        const contentImgs = articleContent.querySelectorAll('img');
        console.log(`文章內容區域找到 ${contentImgs.length} 個圖片`);
        
        contentImgs.forEach((img, index) => {
            contentImages.push({
                index: index + 1,
                src: img.src,
                alt: img.alt,
                srcset: img.srcset
            });
        });
    }
    
    // 5. 檢查 document.images
    const documentImages = Array.from(document.images);
    console.log(`document.images 包含 ${documentImages.length} 個圖片`);
    
    // 6. 返回詳細結果
    const result = {
        page_title: document.title,
        page_url: window.location.href,
        page_ready_state: document.readyState,
        timestamp: new Date().toISOString(),
        
        // 統計
        total_img_elements: allImages.length,
        total_wp_captions: wpCaptions.length,
        total_wp_images: wpImages.length,
        total_content_images: contentImages.length,
        total_document_images: documentImages.length,
        
        // 詳細資料
        all_images: imageDetails,
        wp_images: wpImages,
        content_images: contentImages,
        
        // 除錯資訊
        html_snippet: document.body.innerHTML.substring(0, 1000),
        
        // 測試特定的圖片 URL
        test_image_found: document.querySelector('img[src*="Gr1ks_at_IEM_Cologne"]') ? true : false
    };
    
    console.log('除錯完成，返回結果');
    return result;
    """
    
    crawler_config = CrawlerRunConfig(
        word_count_threshold=1,  # 降低閾值
        excluded_tags=[],  # 不排除任何標籤
        excluded_selector="",  # 不排除任何選擇器
        exclude_external_links=False,
        js_code=debug_js,
        wait_for="css:img",  # 等待圖片載入
        delay_before_return_html=3.0  # 載入後等待3秒
    )
    
    browser_config = BrowserConfig(
        headless=True,
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        print(f"🔗 開始爬取: {url}")
        result = await crawler.arun(url=url, config=crawler_config)
        
        print(f"✅ 爬取完成")
        print(f"📄 頁面標題: {result.metadata.get('title', 'N/A')}")
        
        if result.js_execution_result:
            js_result = result.js_execution_result
            
            print(f"\n📊 圖片統計:")
            print(f"   🖼️ IMG 元素總數: {js_result.get('total_img_elements', 0)}")
            print(f"   🏷️ WordPress 圖片容器: {js_result.get('total_wp_captions', 0)}")
            print(f"   📸 WordPress 圖片: {js_result.get('total_wp_images', 0)}")
            print(f"   📝 內容區域圖片: {js_result.get('total_content_images', 0)}")
            print(f"   📋 document.images: {js_result.get('total_document_images', 0)}")
            print(f"   🎯 測試圖片找到: {js_result.get('test_image_found', False)}")
            
            # 顯示前幾個圖片的詳細資訊
            all_images = js_result.get('all_images', [])
            print(f"\n🔍 前5個圖片詳細資訊:")
            for i, img in enumerate(all_images[:5], 1):
                print(f"   📷 圖片 {i}:")
                print(f"       Src: {img.get('src', 'N/A')}")
                print(f"       Alt: {img.get('alt', 'N/A')}")
                print(f"       Class: {img.get('className', 'N/A')}")
                print(f"       Srcset: {img.get('srcset', 'N/A')[:100]}...")
                print(f"       Complete: {img.get('complete', 'N/A')}")
                print(f"       Parent: {img.get('parentElement', 'N/A')}")
                print()
            
            # 顯示 WordPress 圖片
            wp_images = js_result.get('wp_images', [])
            if wp_images:
                print(f"\n🏷️ WordPress 圖片:")
                for i, wp_img in enumerate(wp_images[:3], 1):
                    print(f"   📸 WP圖片 {i}:")
                    print(f"       容器類別: {wp_img.get('containerClass', 'N/A')}")
                    print(f"       圖片來源: {wp_img.get('imgSrc', 'N/A')}")
                    print(f"       圖片說明: {wp_img.get('imgAlt', 'N/A')}")
                    print()
            
            # 儲存詳細結果
            with open("esports_debug.json", "w", encoding="utf-8") as f:
                json.dump(js_result, f, indent=2, ensure_ascii=False)
            print(f"\n💾 詳細除錯結果已儲存至: esports_debug.json")
            
        else:
            print(f"❌ JavaScript 執行失敗")
            print(f"錯誤資訊: {result.js_execution_result}")

async def main():
    """主函數"""
    print("=" * 60)
    print("🔍 Esports.net 圖片擷取除錯測試")
    print("=" * 60)
    
    try:
        await debug_image_extraction()
        
        print("\n" + "=" * 60)
        print("🎉 除錯測試完成！")
        print("=" * 60)
        print("\n💡 請檢查 esports_debug.json 以了解詳細結果")
        
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
