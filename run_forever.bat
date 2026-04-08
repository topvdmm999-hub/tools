@echo off
:: ป้องกัน Error เรื่องชื่อเจ้าของ
git config --global user.email "bot@price.com"
git config --global user.name "PriceBot"

:loop
cls
echo [%time%] Running Bot...
python super_scraper.py
echo [%time%] Pushing to GitHub...
git add index.html
git commit -m "Auto-update %date% %time%"
git push origin main --force
echo [%time%] Sleeping 10 min...
timeout /t 600
goto loop