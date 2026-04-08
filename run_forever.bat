:loop
python super_scraper.py
git add .
git commit -m "Auto-update from Local Server"
git push
timeout /t 600
goto loop