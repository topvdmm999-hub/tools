@echo off
:: 1. ตั้งค่าตัวตน (แก้ปัญหา 'Please tell me who you are' ในรูปมึง)
git config --global user.email "bot@price-tracker.com"
git config --global user.name "PriceBot"

:loop
cls
echo [%time%] 1. Scraping Data...
python super_scraper.py

echo [%time%] 2. Adding Files...
:: กวาดทุกไฟล์ที่เปลี่ยนแปลงเข้าระบบ
git add .

echo [%time%] 3. Committing...
:: บันทึกการเปลี่ยนแปลง (ถ้าไม่มีคำสั่งนี้มันจะ push ไม่ไปแบบในรูปมึง)
git commit -m "Auto-update: %date% %time%"

echo [%time%] 4. Pushing to GitHub...
:: ใช้ --force เพื่อลุยไฟทับของเก่าไปเลย
git push origin main --force

echo [%time%] Done! Sleeping 10 min...
timeout /t 600
goto loop