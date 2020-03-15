# Copyright (C) Hearot - All Rights Reserved
# Written by Gabriel Hearot <gabriel@hearot.it>.
# See LICENSE.

"""Send charts about italian covid19
expansion via Telegram using a bot."""

import argparse
import datetime
import html
import schedule
import telegram
import time

try:
    from covid import draw_plots, extensions, files, general_excluded_plots #noqa
except (ImportError, ModuleNotFoundError):
    from .covid import draw_plots, extensions, files, general_excluded_plots #noqa

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
        try:
            schedule.run_pending()
        except Exception:
            pass
        time.sleep(60)


def send_charts():
    global ids
    
    data = draw_plots()
    
    for message_id in ids:
        bot.delete_message(chat_id=conf.chat, message_id=message_id)
    
    ids.clear()
    
    for filename in files:
        photos = []
        
        for extension in extensions:
            if not filename == 'general_plot' or extension not in general_excluded_plots:
                try:
                    with open(filename + extension, 'rb') as input_photo:
                        photos.append(
                            telegram.InputMediaPhoto(caption=extensions[extension],
                                                    media=input_photo))
                except Exception:
                    pass
        
        media_ids = [message.message_id for message in 
                     bot.send_media_group(chat_id=conf.chat,
                                          media=photos,
                                          disable_notification=True,
                                          timeout=300)]
            
        if filename == "general_plot":
            ids.append(
                bot.send_message(chat_id=conf.chat,
                                 disable_notification=True,
                                 text="📈 <b>Grafico generale</b>",
                                 parse_mode='HTML',
                                 reply_to_message_id=media_ids[0],
                                 timeout=300).message_id)
        else:
            ids.append(
                bot.send_message(chat_id=conf.chat,
                                 disable_notification=True,
                                 text=("📈 <b>" + filename.replace("_", " ").title() +
                                        "</b> (" + f"{data[-1][filename]:,d}".replace(',', '.') + ", Δ=" +
                                        f"{data[-1][filename]-data[-2][filename]:,d}".replace(',', '.') +
                                        ")"),
                                 parse_mode='HTML',
                                 reply_to_message_id=media_ids[0],
                                 timeout=300).message_id)
            
        ids += media_ids


if __name__ == '__main__':
    main()