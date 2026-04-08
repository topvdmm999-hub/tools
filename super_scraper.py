import requests
from bs4 import BeautifulSoup
import datetime

def get_prices():
    all_data = []
    h = {'User-Agent': 'Mozilla/5.0'}
    
    # Advice
    try:
        r = requests.get("https://www.advice.co.th/product/hot-items", headers=h, timeout=10)
        s = BeautifulSoup(r.content, 'html.parser')
        for item in s.select(".product-item")[:12]:
            name = item.select_one(".product-name").text.strip()
            price = item.select_one(".product-price").text.strip()
            if price != "0": all_data.append({"shop":"ADVICE", "name":name, "price":price})
    except: pass

    # JIB
    try:
        r = requests.get("https://www.jib.co.th/web/product/product_list/1", headers=h, timeout=10)
        s = BeautifulSoup(r.content, 'html.parser')
        for item in s.select(".product_box")[:12]:
            name = item.select_one(".promo_name").text.strip()
            price = item.select_one(".price_total").text.strip()
            if price != "0": all_data.append({"shop":"JIB", "name":name, "price":price})
    except: pass
    
    return all_data

def build_web(data):
    now = (datetime.datetime.now() + datetime.timedelta(hours=7)).strftime("%H:%M:%S")
    
    # สร้างโครงสร้าง HTML ใหม่ทั้งหมด (ไม่ต้องใช้ไฟล์เดิม)
    html = f'''<!DOCTYPE html><html lang="th"><head><meta charset="UTF-8">
    <title>PC Price Tracker</title>
    <script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-slate-950 text-white p-8"><div class="max-w-6xl mx-auto">
    <h1 class="text-4xl font-black text-yellow-500 mb-2">PC HARDWARE TRACKER</h1>
    <p class="text-slate-400 font-mono mb-8 italic">Last Update: {now}</p>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">'''
    
    for i in data:
        color = "blue-600" if i['shop'] == "ADVICE" else "red-600"
        html += f'''<div class="bg-slate-900 border border-slate-800 p-6 rounded-xl hover:border-yellow-500 shadow-lg">
        <span class="bg-{color} text-[10px] px-2 py-0.5 rounded font-bold uppercase">{i['shop']}</span>
        <h3 class="text-sm font-bold my-3 h-10 overflow-hidden text-slate-200">{i['name']}</h3>
        <div class="text-2xl font-black text-yellow-400">{i['price']} THB</div></div>'''
        
    html += '</div></div></body></html>'
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    print("Scraping Data...")
    items = get_prices()
    if items:
        build_web(items)
        print(f"Update Success! {len(items)} items.")
    else:
        print("Error: No data found.")