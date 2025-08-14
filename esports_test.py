#!/usr/bin/env python3
"""
電競新聞網站爬取測試 - 專門針對 esports.net
"""

import asyncio
import json
import re
import os
import aiohttp
import aiofiles
import ssl
from datetime import datetime
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig

async def download_image(session, url, file_path, semaphore):
    """下載單張圖片"""
    async with semaphore:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.read()
                    async with aiofiles.open(file_path, 'wb') as f:
                        await f.write(content)
                    return {"url": url, "file_path": file_path, "status": "success", "size": len(content)}
                else:
                    return {"url": url, "file_path": file_path, "status": "failed", "error": f"HTTP {response.status}"}
        except Exception as e:
            return {"url": url, "file_path": file_path, "status": "failed", "error": str(e)}

async def download_images_batch(images, base_folder, test_name):
    """批量下載圖片"""
    # 建立資料夾名稱：測試名稱+image+執行時間
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"{test_name}_images_{timestamp}"
    images_folder = os.path.join(base_folder, folder_name)
    
    # 建立資料夾
    os.makedirs(images_folder, exist_ok=True)
    print(f"📁 建立圖片資料夾: {folder_name}")
    
    # 建立 HTTP session 和 semaphore（限制併發）
    semaphore = asyncio.Semaphore(5)  # 最多同時下載5張圖片
    
    # 建立 SSL 配置（跳過證書驗證）
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    connector = aiohttp.TCPConnector(limit=10, ssl=ssl_context)
    timeout = aiohttp.ClientTimeout(total=30)
    
    download_results = []
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = []
        
        for i, img in enumerate(images, 1):
            img_url = img.get('src', '')
            if not img_url or img_url.startswith('data:'):
                continue
            
            # 從 URL 獲取檔案副檔名
            try:
                file_extension = img_url.split('.')[-1].split('?')[0].lower()
                if file_extension not in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg']:
                    file_extension = 'jpg'  # 預設為 jpg
            except:
                file_extension = 'jpg'
            
            # 建立檔案名稱
            img_alt = img.get('alt', '').replace('/', '_').replace('\\', '_')[:50]  # 限制長度並移除特殊字元
            filename = f"img_{i:03d}_{img_alt}_{timestamp}.{file_extension}"
            filename = "".join(c for c in filename if c.isalnum() or c in '._-')  # 只保留安全字元
            
            file_path = os.path.join(images_folder, filename)
            
            # 建立下載任務
            task = download_image(session, img_url, file_path, semaphore)
            tasks.append((task, img_url, filename, img))
        
        print(f"🚀 開始下載 {len(tasks)} 張圖片...")
        
        # 執行所有下載任務
        for i, (task, url, filename, img_info) in enumerate(tasks, 1):
            try:
                result = await task
                download_results.append({
                    'index': i,
                    'filename': filename,
                    'url': url,
                    'alt': img_info.get('alt', ''),
                    'success': result['status'] == 'success',
                    'error': result.get('error', ''),
                    'size': result.get('size', 0)
                })
                
                if result['status'] == 'success':
                    print(f"   ✅ ({i}/{len(tasks)}) {filename} - {result.get('size', 0)} bytes")
                else:
                    print(f"   ❌ ({i}/{len(tasks)}) {filename} - {result.get('error', '')}")
                    
            except Exception as e:
                print(f"   💥 ({i}/{len(tasks)}) {filename} - 下載異常: {str(e)}")
                download_results.append({
                    'index': i,
                    'filename': filename,
                    'url': url,
                    'alt': img_info.get('alt', ''),
                    'success': False,
                    'error': str(e),
                    'size': 0
                })
    
    # 統計結果
    successful_downloads = sum(1 for r in download_results if r['success'])
    print(f"\n📊 下載完成統計:")
    print(f"   ✅ 成功: {successful_downloads} 張")
    print(f"   ❌ 失敗: {len(download_results) - successful_downloads} 張")
    print(f"   📁 儲存位置: {images_folder}")
    
    # 儲存下載報告（使用相對路徑）
    report_path = os.path.join(images_folder, "download_report.json")
    # 取得相對於當前工作目錄的路徑
    relative_folder_path = os.path.relpath(images_folder)
    relative_report_path = os.path.relpath(report_path)
    
    async with aiofiles.open(report_path, 'w', encoding='utf-8') as f:
        await f.write(json.dumps({
            'test_name': test_name,
            'timestamp': timestamp,
            'folder_path': relative_folder_path,  # 使用相對路徑
            'total_images': len(download_results),
            'successful_downloads': successful_downloads,
            'failed_downloads': len(download_results) - successful_downloads,
            'download_results': download_results
        }, indent=2, ensure_ascii=False))
    
    print(f"   📄 下載報告: {relative_report_path}")
    
    return images_folder, download_results

async def esports_news_test():
    """電競新聞文章和圖片擷取測試"""
    print("🎮 開始電競新聞網站測試...")
    
    url = "https://www.esports.net/news/counter-strike/cs2-roster-shake-up-heroic-benches-gr1ks-fut-signs-ex-navi-juniors-with-misutaaa/"
    
    # 設定爬蟲參數
    crawler_config = CrawlerRunConfig(
        word_count_threshold=10,
        excluded_tags=[
            "script",
            "footer", 
            "link",
            "iframe"
        ],
        excluded_selector="[class^='_mentions'],[class='container__bannerZone'],[class^='_topBanner'],[class^='_wallpaperBanner'],[id^='lsadvert'],[class^='_newsSection']",
        exclude_external_links=False,
        screenshot=True,  # 開啟截圖功能
    )
    
    # 設定瀏覽器參數
    browser_config = BrowserConfig(
        headless=True
    )
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        print(f"📰 正在爬取電競新聞: {url}")
        
        result = await crawler.arun(
            url=url,
            config=crawler_config
        )
        
        print(f"✅ 爬取完成！")
        print(f"📄 頁面標題: {result.metadata.get('title', 'N/A')}")
        print(f"🔗 URL: {result.url}")
        print(f"📝 內容長度: {len(result.markdown)} 字元")
        
        # 顯示文章內容預覽
        if result.markdown:
            print(f"\n📖 文章內容預覽:")
            print("-" * 60)
            preview = result.markdown[:800] + "..." if len(result.markdown) > 800 else result.markdown
            print(preview)
            print("-" * 60)
        
        # 處理圖片 - 使用內建的 media 屬性
        print(f"\n🖼️ 內建圖片擷取結果:")
        if hasattr(result, 'media') and result.media and 'images' in result.media:
            images = result.media['images']
            print(f"   找到 {len(images)} 張圖片")
            
            # 顯示前10張圖片資訊
            for i, img in enumerate(images[:10], 1):
                print(f"   📷 圖片 {i}: {img.get('src', 'N/A')}")
                print(f"       Alt: {img.get('alt', 'N/A')}")
                print(f"       尺寸: {img.get('width', 'N/A')} x {img.get('height', 'N/A')}")
                print()
            
            # 下載所有圖片
            print(f"\n📥 開始下載圖片...")
            images_folder, download_results = await download_images_batch(
                images, 
                ".", 
                "esports_news"
            )
            
        else:
            print(f"   ❌ 內建圖片擷取未找到圖片")
            print(f"   Media 屬性: {hasattr(result, 'media')}")
            if hasattr(result, 'media'):
                print(f"   Media 內容: {result.media}")
        
        # 處理圖片 - 從 HTML 內容中手動解析
        print(f"\n🔍 手動解析 HTML 中的圖片:")
        if result.cleaned_html:
            import re
            # 使用正規表達式找出所有 img 標籤
            img_pattern = r'<img[^>]*src=["\'](.*?)["\'][^>]*alt=["\'](.*?)["\'][^>]*>'
            img_matches = re.findall(img_pattern, result.cleaned_html, re.IGNORECASE)
            
            print(f"   找到 {len(img_matches)} 個圖片標籤")
            for i, (src, alt) in enumerate(img_matches[:5], 1):
                print(f"   📷 HTML圖片 {i}:")
                print(f"       來源: {src}")
                print(f"       說明: {alt}")
                print()
        
        # 處理更複雜的 img 標籤解析
        if result.cleaned_html:
            # 更完整的圖片解析
            img_complex_pattern = r'<img[^>]*>'
            complex_matches = re.findall(img_complex_pattern, result.cleaned_html, re.IGNORECASE)
            print(f"   🔍 總共找到 {len(complex_matches)} 個 img 標籤")
            
            # 解析每個 img 標籤的屬性
            for i, img_tag in enumerate(complex_matches[:5], 1):
                src_match = re.search(r'src=["\'](.*?)["\']', img_tag, re.IGNORECASE)
                alt_match = re.search(r'alt=["\'](.*?)["\']', img_tag, re.IGNORECASE)
                class_match = re.search(r'class=["\'](.*?)["\']', img_tag, re.IGNORECASE)
                
                print(f"   📷 複雜解析 {i}:")
                print(f"       標籤: {img_tag[:100]}...")
                print(f"       來源: {src_match.group(1) if src_match else 'N/A'}")
                print(f"       說明: {alt_match.group(1) if alt_match else 'N/A'}")
                print(f"       類別: {class_match.group(1) if class_match else 'N/A'}")
                print()
        
        # 儲存截圖
        if result.screenshot:
            screenshot_path = "esports_screenshot.png"
            if isinstance(result.screenshot, str):
                # 如果是 base64 字串，需要解碼
                import base64
                screenshot_data = base64.b64decode(result.screenshot)
            else:
                # 如果已經是 bytes
                screenshot_data = result.screenshot
                
            with open(screenshot_path, "wb") as f:
                f.write(screenshot_data)
            print(f"📸 頁面截圖已儲存至: esports_screenshot.png")
        
        # 分析連結
        if result.links:
            internal_links = result.links.get('internal', [])
            external_links = result.links.get('external', [])
            
            print(f"\n🔗 連結分析:")
            print(f"   🏠 內部連結: {len(internal_links)} 個")
            print(f"   🌐 外部連結: {len(external_links)} 個")
            
            if internal_links:
                print(f"\n📋 相關文章連結 (前5個):")
                for i, link in enumerate(internal_links[:5], 1):
                    print(f"   {i}. {link}")
        
        # 儲存完整結果到檔案
        result_data = {
            'title': result.metadata.get('title', ''),
            'url': result.url,
            'content_length': len(result.markdown),
            'images_count': len(result.media.get('images', [])) if hasattr(result, 'media') and result.media else 0,
            'internal_links_count': len(result.links.get('internal', [])) if result.links else 0,
            'external_links_count': len(result.links.get('external', [])) if result.links else 0,
            'content_preview': result.markdown[:1000] if result.markdown else '',
            'timestamp': '2025-08-14'
        }
        
        with open("esports_result.json", "w", encoding="utf-8") as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 完整結果已儲存至: esports_result.json")

async def esports_with_css_selector_test():
    """使用 CSS 選擇器專門擷取文章內容"""
    print("\n🎯 使用 CSS 選擇器測試...")
    
    url = "https://www.esports.net/news/counter-strike/cs2-roster-shake-up-heroic-benches-gr1ks-fut-signs-ex-navi-juniors-with-misutaaa/"
    
    # 針對 esports.net 的文章選擇器
    css_selectors = [
        "article .content",  # 文章內容
        ".article-content",  # 可能的文章容器
        "[class*='article']", # 包含 article 的 class
        ".post-content",     # 可能的文章內容
        "main article"       # 主要文章區域
    ]
    
    crawler_config = CrawlerRunConfig(
        word_count_threshold=10,
        excluded_tags=["script", "footer", "link", "iframe"],
        excluded_selector="[class^='_mentions'],[class='container__bannerZone'],[class^='_topBanner'],[class^='_wallpaperBanner'],[id^='lsadvert'],[class^='_newsSection']",
        exclude_external_links=False
    )
    
    browser_config = BrowserConfig(headless=True)
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        for i, selector in enumerate(css_selectors, 1):
            try:
                print(f"🔍 測試選擇器 {i}: {selector}")
                
                config_with_selector = CrawlerRunConfig(
                    word_count_threshold=10,
                    excluded_tags=["script", "footer", "link", "iframe"],
                    excluded_selector="[class^='_mentions'],[class='container__bannerZone'],[class^='_topBanner'],[class^='_wallpaperBanner'],[id^='lsadvert'],[class^='_newsSection']",
                    exclude_external_links=False,
                    css_selector=selector
                )
                
                result = await crawler.arun(
                    url=url,
                    config=config_with_selector
                )
                
                if result.markdown and len(result.markdown) > 100:
                    print(f"   ✅ 成功擷取 {len(result.markdown)} 字元")
                    preview = result.markdown[:200] + "..." if len(result.markdown) > 200 else result.markdown
                    print(f"   📖 內容: {preview}")
                    print()
                else:
                    print(f"   ❌ 擷取內容過少或失敗")
                    print()
                    
            except Exception as e:
                print(f"   ❌ 選擇器失敗: {str(e)}")
                print()

async def esports_images_extraction_test():
    """專門擷取圖片的測試"""
    print("\n🖼️ 專門圖片擷取測試...")
    
    url = "https://www.esports.net/news/counter-strike/cs2-roster-shake-up-heroic-benches-gr1ks-fut-signs-ex-navi-juniors-with-misutaaa/"
    
    # 改良的 JavaScript 代碼來擷取頁面中的所有圖片
    js_code = """
    // 等待圖片載入
    await new Promise(resolve => {
        if (document.readyState === 'complete') {
            resolve();
        } else {
            window.addEventListener('load', resolve);
        }
    });
    
    // 等待額外的時間讓動態內容載入
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 獲取所有圖片，包括 srcset 中的圖片
    const images = [];
    const imgElements = document.querySelectorAll('img');
    
    imgElements.forEach((img, index) => {
        const imageData = {
            index: index + 1,
            src: img.src || '',
            alt: img.alt || '',
            width: img.naturalWidth || img.width || 'N/A',
            height: img.naturalHeight || img.height || 'N/A',
            className: img.className || '',
            id: img.id || '',
            title: img.title || '',
            srcset: img.srcset || '',
            loading: img.loading || '',
            decoding: img.decoding || '',
            fetchpriority: img.getAttribute('fetchpriority') || ''
        };
        
        // 不過濾任何圖片，包括 data: 開頭的
        images.push(imageData);
        
        // 如果有 srcset，也提取其中的 URL
        if (img.srcset) {
            const srcsetUrls = img.srcset.split(',').map(entry => {
                const parts = entry.trim().split(' ');
                return {
                    url: parts[0],
                    width: parts[1] || 'N/A'
                };
            });
            imageData.srcset_urls = srcsetUrls;
        }
    });
    
    // 也查找背景圖片
    const elementsWithBackground = document.querySelectorAll('*');
    const backgroundImages = [];
    
    elementsWithBackground.forEach((el, index) => {
        const style = window.getComputedStyle(el);
        const backgroundImage = style.backgroundImage;
        
        if (backgroundImage && backgroundImage !== 'none') {
            const urlMatch = backgroundImage.match(/url\\(["']?([^"')]+)["']?\\)/);
            if (urlMatch) {
                backgroundImages.push({
                    index: index + 1,
                    element: el.tagName.toLowerCase(),
                    className: el.className,
                    backgroundImage: urlMatch[1]
                });
            }
        }
    });
    
    const result = {
        page_title: document.title,
        page_url: window.location.href,
        total_images: images.length,
        total_background_images: backgroundImages.length,
        images: images,
        background_images: backgroundImages,
        document_ready_state: document.readyState,
        timestamp: new Date().toISOString()
    };
    
    return result;
    """
    
    crawler_config = CrawlerRunConfig(
        word_count_threshold=10,
        excluded_tags=["script", "footer", "link"],  # 移除 iframe，因為可能包含圖片
        excluded_selector="[class^='_mentions'],[class='container__bannerZone'],[class^='_topBanner'],[class^='_wallpaperBanner'],[id^='lsadvert'],[class^='_newsSection']",
        exclude_external_links=False,
        js_code=js_code,
        wait_for="css:img"  # 等待圖片元素載入
    )
    
    browser_config = BrowserConfig(headless=True)
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url=url,
            config=crawler_config
        )
        
        print(f"✅ JavaScript 圖片擷取完成")
        
        if result.js_execution_result:
            js_result = result.js_execution_result
            
            # 處理 Crawl4AI 的結果格式
            if isinstance(js_result, dict) and 'results' in js_result and js_result['results']:
                actual_result = js_result['results'][0]
            else:
                actual_result = js_result
            
            print(f"🖼️ 找到 {actual_result.get('total_images', 0)} 張圖片")
            print(f"🎨 找到 {actual_result.get('total_background_images', 0)} 張背景圖片")
            print(f"📄 頁面狀態: {actual_result.get('document_ready_state', 'N/A')}")
            
            images = actual_result.get('images', [])
            for i, img in enumerate(images[:10], 1):  # 顯示前10張
                print(f"   📷 圖片 {i}:")
                print(f"       來源: {img.get('src', 'N/A')}")
                print(f"       說明: {img.get('alt', 'N/A')}")
                print(f"       尺寸: {img.get('width', 'N/A')} x {img.get('height', 'N/A')}")
                print(f"       CSS類別: {img.get('className', 'N/A')}")
                if img.get('srcset'):
                    print(f"       Srcset: {img.get('srcset', 'N/A')[:100]}...")
                print()
            
            # 下載 JavaScript 擷取的圖片
            if images:
                print(f"\n📥 下載 JavaScript 擷取的圖片...")
                js_images_folder, js_download_results = await download_images_batch(
                    images, 
                    ".", 
                    "esports_js"
                )
            
            # 顯示背景圖片
            bg_images = actual_result.get('background_images', [])
            if bg_images:
                print(f"\n🎨 背景圖片:")
                for i, bg in enumerate(bg_images[:5], 1):
                    print(f"   🖼️ 背景 {i}: {bg.get('backgroundImage', 'N/A')}")
            
            # 儲存圖片資訊
            with open("esports_images.json", "w", encoding="utf-8") as f:
                json.dump(actual_result, f, indent=2, ensure_ascii=False)
            print(f"\n💾 圖片資訊已儲存至: esports_images.json")
        else:
            print(f"❌ JavaScript 執行失敗或無結果")
            print(f"執行結果: {result.js_execution_result}")

async def main():
    """主函數"""
    print("=" * 60)
    print("🎮 電競新聞網站專門測試")
    print("=" * 60)
    
    try:
        await esports_news_test()
        await esports_with_css_selector_test()
        await esports_images_extraction_test()
        
        print("\n" + "=" * 60)
        print("🎉 所有電競新聞測試完成！")
        print("=" * 60)
        print("\n📁 生成的檔案:")
        print("   📄 esports_result.json - 完整結果資料")
        print("   🖼️ esports_images.json - 圖片資訊")
        print("   📸 esports_screenshot.png - 頁面截圖")
        print("   📁 images/ - 圖片資料夾")
        
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
