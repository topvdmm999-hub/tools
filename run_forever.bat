@echo off
:loop
python super_scraper.py
git add .
git commit -m "Auto-update prices"
git push origin main --force
timeout /t 600
goto loop