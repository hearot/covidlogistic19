# Copyright (C) Hearot - All Rights Reserved
# Written by Gabriel Hearot <gabriel@hearot.it>.

"""Send charts about italian covid19
expansion via Telegram using a bot."""

import argparse
import datetime
import glob
import html
import schedule
import telegram
import time

try:
    from covid import draw_plots #noqa
except (ImportError, ModuleNotFoundError):
    from .covid import draw_plots #noqa

try:
    try:
        from . import conf #noqa
    except (ImportError, ModuleNotFoundError):
        import conf
except (ImportError, ModuleNotFoundError):
    print("Edit _conf.py and then rename it to conf.py!")
    exit(1)


bot = telegram.Bot(token=conf.token)
ids = []


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-n', '--now', dest='now', 
                        action='store_true', default=False,
                        help='send now the charts')

    args = parser.parse_args()
    schedule.every().day.at(conf.time).do(send_charts)
    
    if args.now:
        send_charts()
    
    while True:
        schedule.run_pending()
        time.sleep(60)


def send_charts():
    global ids
    
    data = draw_plots()
    
    for message_id in ids:
        bot.delete_message(chat_id=conf.chat, message_id=message_id)
    
    ids.clear()
    
    for filename in sorted(glob.glob("./*.png")):
        with open(filename, 'rb') as file:
            parameter = filename.replace(".png", "")[2:]
            
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
                                         " (" + f"{data[-1][parameter]:,d}".replace(',', '.') + ", Δ=" +
                                         f"{data[-1][parameter]-data[-2][parameter]:,d}".replace(',', '.') +
                                         ")")).message_id)


if __name__ == '__main__':
    main()