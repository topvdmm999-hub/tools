import requests
from bs4 import BeautifulSoup
import datetime
import random

def get_prices():
    all_data = []
    h = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # Advice
    try:
        r = requests.get("https://www.advice.co.th/product/hot-items", headers=h, timeout=15)
        s = BeautifulSoup(r.content, 'html.parser')
        for item in s.select(".product-item")[:10]:
            name = item.select_one(".product-name").text.strip()
            price = item.select_one(".product-price").text.strip()
            if price != "0": all_data.append({"shop":"ADVICE", "name":name, "price":price})
    except Exception as e: print(f"Advice Error: {e}")

    # JIB
    try:
        r = requests.get("https://www.jib.co.th/web/product/product_list/1", headers=h, timeout=15)
        s = BeautifulSoup(r.content, 'html.parser')
        for item in s.select(".product_box")[:10]:
            name = item.select_one(".promo_name").text.strip()
            price = item.select_one(".price_total").text.strip()
            if price != "0": all_data.append({"shop":"JIB", "name":name, "price":price})
    except Exception as e: print(f"JIB Error: {e}")
    
    return all_data

def build_web(data):
    # แก้เวลาให้ตรงกับไทย และเพิ่มเลขสุ่มกัน Cache
    now = (datetime.datetime.now() + datetime.timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S")
    v = random.randint(1000, 9999)
    
    html = f'''<!DOCTYPE html><html lang="th"><head><meta charset="UTF-8">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <title>Price Update {v}</title>
    <script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-zinc-950 text-white p-6"><div class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-black text-yellow-500 mb-2 underline decoration-yellow-500/30">LIVE PC PRICES</h1>
    <p class="text-zinc-500 mb-8 font-mono italic">Last Update: {now} (v.{v})</p>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">'''
    
    for i in data:
        # แก้ไขการเช็คชื่อร้านให้เป๊ะขึ้น
        is_advice = "ADVICE" in i['shop'].upper()
        shop_color = "blue-600" if is_advice else "red-600"
        
        html += f'''<div class="bg-zinc-900 border border-zinc-800 p-4 rounded-xl shadow-lg">
        <span class="inline-block bg-{shop_color} text-[10px] px-2 py-0.5 rounded font-bold mb-2">{i['shop']}</span>
        <div class="text-sm font-medium mb-2 text-zinc-300 h-10 overflow-hidden">{i['name']}</div>
        <div class="text-xl font-bold text-yellow-400">{i['price']} THB</div></div>'''
        
    html += '</div></div><script>console.log("Updated at ' + now + '")</script></body></html>'
    
    # บันทึกไฟล์ลง D:\checkraka\index.html
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    print("--- บอทกำลังเริ่มทำงาน ---")
    items = get_prices()
    if items:
        build_web(items)
        print(f"Success! {len(items)} items found and index.html updated.")
    else:
        print("Error: ขูดข้อมูลไม่ได้เลยสักอัน!")