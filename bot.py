# Copyright (C) Hearot - All Rights Reserved
# Written by Gabriel Hearot <gabriel@hearot.it>.

import datetime
import glob
import html
import schedule
import telegram
import time

try:
    from covidlogistic19 import main
except (ImportError, ModuleNotFoundError):
    from .covidlogistic19 import main

try:
    try:
        from . import conf
    except (ImportError, ModuleNotFoundError):
        import conf
except (ImportError, ModuleNotFoundError):
    print("Edit _conf.py and then rename it to conf.py!")
    exit(1)


bot = telegram.Bot(token=conf.token)
ids = []

def send_charts():
    global ids
    
    data = main()
    
    for message_id in ids:
        bot.delete_message(chat_id=conf.chat, message_id=message_id)
    
    ids.clear()
    
    for filename in glob.glob("./*.png"):
        with open(filename, 'rb') as file:
            parameter = filename.replace(".png", "").replace(".\\", "")
            
            if parameter == "general_plot":
                ids.append(
                    bot.send_photo(chat_id=conf.chat,
                                photo=file, 
                                caption="📈 Grafico generale").message_id)
            else:
                ids.append(
                    bot.send_photo(chat_id=conf.chat,
                                photo=file, 
                                caption=("📈 " + parameter.replace("_", " ").title() +
                                         " (" + f"{data[-1][parameter]:,d}".replace(',', '.') + ")")).message_id)


schedule.every().day.at(conf.time).do(send_charts)

while True:
    schedule.run_pending()
    time.sleep(60)