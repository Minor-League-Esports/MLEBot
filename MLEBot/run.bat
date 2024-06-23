@echo on

call .\.venv\Scripts\activate.bat

python -m pip install --upgrade PyDiscoBot

python mle_bot.py

PAUSE