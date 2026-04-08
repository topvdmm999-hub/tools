import requests
from bs4 import BeautifulSoup
import datetime

def get_prices():
    all_data = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    
    # --- ADVICE ---
    try:
        r = requests.get("https://www.advice.co.th/product/hot-items", headers=headers, timeout=10)
        s = BeautifulSoup(r.content, 'html.parser')
        # ใช้ Selector ที่กว้างขึ้นเพื่อให้ครอบคลุม
        items = s.select(".product-item, .item-list")
        for item in items[:10]:
            name = item.select_one(".product-name, .name")
            price = item.select_one(".product-price, .price")
            if name and price:
                all_data.append({"shop": "ADVICE", "name": name.get_text(strip=True), "price": price.get_text(strip=True)})
    except: pass

    # --- JIB ---
    try:
        r = requests.get("https://www.jib.co.th/web/product/product_list/1", headers=headers, timeout=10)
        s = BeautifulSoup(r.content, 'html.parser')
        items = s.select(".product_box")
        for item in items[:10]:
            name = item.select_one(".promo_name, .name_product")
            price = item.select_one(".price_total, .price_total_product")
            if name and price:
                all_data.append({"shop": "JIB", "name": name.get_text(strip=True), "price": price.get_text(strip=True)})
    except: pass
    
    return all_data

def build_web(data):
    now = (datetime.datetime.now() + datetime.timedelta(hours=7)).strftime("%H:%M:%S")
    cards = ""
    if not data:
        cards = '<div class="col-span-full text-center py-20 border-2 border-dashed border-red-500 rounded-2xl text-red-500 font-bold">❌ ขูดไม่ติด (Check Selectors)</div>'
    else:
        for i in data:
            bg = "blue-600" if i['shop'] == "ADVICE" else "red-600"
            cards += f'''<div class="bg-zinc-900 border border-zinc-800 p-5 rounded-2xl">
            <span class="bg-{bg} text-[10px] px-2 py-0.5 rounded font-black uppercase">{i['shop']}</span>
            <div class="text-sm font-bold my-3 text-zinc-300 h-10 overflow-hidden">{i['name']}</div>
            <div class="text-2xl font-black text-yellow-400">{i['price']} <span class="text-xs text-zinc-600">THB</span></div></div>'''

    html = f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-black text-white p-6 font-sans"><div class="max-w-5xl mx-auto">
    <div class="flex justify-between items-center mb-8"><h1 class="text-4xl font-black text-yellow-500 italic">PRICE BOT v2</h1><p class="font-mono text-zinc-500">Sync: {now}</p></div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">{cards}</div></div></body></html>'''
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(html)

if __name__ == "__main__":
    res = get_prices()
    build_web(res)
    print(f"Success! Found {len(res)} items.")