import requests
from bs4 import BeautifulSoup
import json
import datetime

def scrape_data():
    all_items = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # ส่อง Advice
    try:
        res = requests.get("https://www.advice.co.th/product/hot-items", headers=headers, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        for p in soup.select(".product-item")[:10]:
            name = p.select_one(".product-name").text.strip()
            price = p.select_one(".product-price").text.strip()
            if "0" != price and "N/A" not in price:
                all_items.append({"shop": "ADVICE", "name": name, "price": price})
    except: print("Advice Error")

    # ส่อง JIB
    try:
        res = requests.get("https://www.jib.co.th/web/product/product_list/1", headers=headers, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        for p in soup.select(".product_box")[:10]:
            name = p.select_one(".promo_name").text.strip()
            price = p.select_one(".price_total").text.strip()
            if price and "0" != price:
                all_items.append({"shop": "JIB", "name": name, "price": price})
    except: print("JIB Error")

    # บันทึกลงไฟล์ JSON เพื่อให้หน้าเว็บดึงไปใช้
    result = {
        "updated": (datetime.datetime.now() + datetime.timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S"),
        "items": all_items
    }
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    print(f"ขูดเสร็จแล้ว! เจอ {len(all_items)} รายการ")

if __name__ == "__main__":
    scrape_data()