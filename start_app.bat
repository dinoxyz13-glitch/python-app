@echo off
rem AI writing tool launcher (double-click, or put a shortcut in the Startup folder)
cd /d "%~dp0"
python -m streamlit run app.py
rem Keep the window open so any error message stays readable
pause
