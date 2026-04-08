@echo off
:loop
echo [%time%] Starting Scraper...
python super_scraper.py
echo [%time%] Pushing to GitHub...
git add .
git commit -m "Auto-update data"
git push origin main --force
echo [%time%] Waiting 10 minutes...
timeout /t 600
goto loop