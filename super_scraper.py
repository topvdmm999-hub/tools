import requests
from bs4 import BeautifulSoup
import datetime
import re

def scrape_store(url, item_selector, name_selector, price_selector, shop_name):
    print(f"กำลังขูด {shop_name}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    results = []
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        items = soup.select(item_selector)[:8] # เอา 8 ตัวแรกของหน้า
        for item in items:
            name = item.select_one(name_selector).text.strip()
            price = item.select_one(price_selector).text.strip()
            # กรองคำว่า "ไม่มีสินค้า" ออกไป
            if "ไม่มี" not in price and "N/A" not in price:
                results.append({"shop": shop_name, "name": name, "price": price})
    except Exception as e:
        print(f"Error {shop_name}: {e}")
    return results

if __name__ == "__main__":
    # มึงเพิ่ม URL หมวดหมู่ที่มึงสนใจได้ตรงนี้เลย (จอ, RAM, SSD)
    data = []
    data += scrape_store("https://www.advice.co.th/product/hot-items", ".product-item", ".product-name", ".product-price", "ADVICE")
    data += scrape_store("https://www.jib.co.th/web/product/product_list/1", ".product_box", ".promo_name", ".price_total", "JIB")

    if data:
        html_cards = ""
        for i in data:
            html_cards += f'''
            <div class="bg-slate-800 p-6 rounded-xl border border-slate-700 hover:border-yellow-500 shadow-lg">
                <span class="bg-blue-600 text-[10px] px-2 py-0.5 rounded text-white font-bold">{i['shop']}</span>
                <h3 class="text-sm font-bold text-white my-2 h-10 overflow-hidden">{i['name']}</h3>
                <p class="text-2xl font-mono text-green-400">{i['price']} THB</p>
            </div>'''
        
        # เขียนลงไฟล์ index.html (ตรวจสอบให้แน่ใจว่าในไฟล์มี Comment )
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        now = (datetime.datetime.now() + datetime.timedelta(hours=7)).strftime("%H:%M:%S")
        updated = re.sub(r'.*?', f'\n{html_cards}\n', content, flags=re.DOTALL)
        updated = re.sub(r'id="status".*?</p>', f'id="status" class="text-slate-400 font-mono italic">Server อัปเดตล่าสุด: {now}</p>', updated)
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(updated)
        print("Done!")