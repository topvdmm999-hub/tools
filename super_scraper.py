import requests
from bs4 import BeautifulSoup
import datetime
import re

def get_advice():
    print("กำลังส่อง Advice...")
    url = "https://www.advice.co.th/product/hot-items"
    headers = {'User-Agent': 'Mozilla/5.0'}
    items_list = []
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        products = soup.select(".product-item")[:12]
        for p in products:
            name = p.select_one(".product-name").text.strip()
            price = p.select_one(".product-price").text.strip()
            if "N/A" not in price and "0" != price:
                items_list.append({"shop": "ADVICE", "name": name, "price": price})
    except: pass
    return items_list

def get_jib():
    print("กำลังส่อง JIB...")
    url = "https://www.jib.co.th/web/product/product_list/1"
    headers = {'User-Agent': 'Mozilla/5.0'}
    items_list = []
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        products = soup.select(".product_box")[:12]
        for p in products:
            name = p.select_one(".promo_name").text.strip()
            price = p.select_one(".price_total").text.strip()
            if price and "0" != price:
                items_list.append({"shop": "JIB", "name": name, "price": price})
    except: pass
    return items_list

if __name__ == "__main__":
    all_items = get_advice() + get_jib()
    html_cards = ""
    for item in all_items:
        color = "blue-600" if item['shop'] == "ADVICE" else "red-600"
        html_cards += f'''
        <div class="bg-slate-800 p-4 rounded-lg border-l-4 border-{color}">
            <div class="text-xs font-bold text-{color}">{item['shop']}</div>
            <div class="text-sm my-1">{item['name']}</div>
            <div class="text-xl font-bold text-yellow-400">{item['price']} THB</div>
        </div>
        '''
    
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    now = (datetime.datetime.now() + datetime.timedelta(hours=7)).strftime("%H:%M:%S")
    content = re.sub(r'.*', f'\n{html_cards}', content, flags=re.DOTALL)
    content = re.sub(r'id="status".*?>.*?<', f'id="status" class="text-slate-400 font-mono italic mb-8">Server Online - อัปเดตล่าสุด: {now}<', content)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"อัปเดตเสร็จแล้ว {len(all_items)} รายการ!")