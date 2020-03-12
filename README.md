# [covidlogistic19](https://t.me/covidstats)

[![License: Creative Commons Attribution 4.0](https://img.shields.io/badge/License-Creative%20Commons%20Attribution%204.0%20International-blue.svg)](./LICENSE) [![Hearot](https://img.shields.io/badge/Developer-%20@hearot-blue.svg)](https://t.me/hearot)

A Telegram bot which allows you to retrieve data from [Dati COVID-19 Italia del Dipartimento della Protezione Civile](https://github.com/pcm-dpc/COVID-19).

To run the bot by yourself, you need:
- Python (tested with 3.8)
- [matplotlib](https://github.com/matplotlib/matplotlib)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [schedule](https://github.com/dbader/schedule)

## Setup
- Get a token from [@BotFather](http://telegram.me/BotFather).
- Install the requirements (using `virtualenv` is recommended) by typing `pip install -r requirements.txt`.
- Edit `_conf.py` with your settings and then rename the file to `conf.py`.
- Run the bot by typing `python bot.py`.