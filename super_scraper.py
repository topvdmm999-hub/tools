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
        for item in s.select(".product-item")[:10]:
            name = item.select_one(".product-name").text.strip()
            price = item.select_one(".product-price").text.strip()
            if price != "0": all_data.append({"shop":"ADVICE", "name":name, "price":price})
    except: pass

    # JIB
    try:
        r = requests.get("https://www.jib.co.th/web/product/product_list/1", headers=h, timeout=10)
        s = BeautifulSoup(r.content, 'html.parser')
        for item in s.select(".product_box")[:10]:
            name = item.select_one(".promo_name").text.strip()
            price = item.select_one(".price_total").text.strip()
            if price != "0": all_data.append({"shop":"JIB", "name":name, "price":price})
    except: pass
    
    return all_data

def build_web(data):
    now = (datetime.datetime.now() + datetime.timedelta(hours=7)).strftime("%H:%M:%S")
    html = f'''<!DOCTYPE html><html lang="th"><head><meta charset="UTF-8"><title>Price Tracking</title>
    <script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-zinc-950 text-white p-6"><div class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-black text-yellow-500 mb-2">LIVE PC PRICES</h1>
    <p class="text-zinc-500 mb-8 font-mono italic">Last Bot Update: {now}</p>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">'''
    
    for i in data:
        shop_color = "blue-600" if i['shop'] == "ADVICE" else "red-600"
        html += f'''<div class="bg-zinc-900 border border-zinc-800 p-4 rounded-xl shadow-lg hover:border-yellow-500">
        <span class="bg-{shop_color} text-[10px] px-2 py-0.5 rounded font-bold">{i['shop']}</span>
        <div class="text-sm font-medium my-2 text-zinc-300">{i['name']}</div>
        <div class="text-xl font-bold text-yellow-400">{i['price']} THB</div></div>'''
        
    html += '</div></div></body></html>'
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    items = get_prices()
    if items:
        build_web(items)
        print(f"Success! {len(items)} items updated.")