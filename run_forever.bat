@echo off
:loop
cls
echo [%time%] 1. Scraping Data...
python super_scraper.py

echo [%time%] 2. Preparing Files for GitHub...
:: คำสั่งนี้จะแก้ปัญหา "Changes not staged" ในรูปของมึง
git add .

echo [%time%] 3. Committing Changes...
git commit -m "Auto-update: %date% %time%"

echo [%time%] 4. Pushing to GitHub...
:: ใช้ force เพื่อให้มันทับของเก่าไปเลย ไม่ต้องรอ pull
git push origin main --force

echo [%time%] Done! Waiting 10 minutes for next update...
timeout /t 600
goto loop