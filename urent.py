#!/usr/bin/env python

import logging
import time
import json
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from math import radians, cos, sin, asin, sqrt
options = webdriver.ChromeOptions()
options.add_argument("headless")

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Telegram Command
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text("你真的知道這是在做什麼嗎？")


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("給我地址或是經緯度！")

def search_location(update: Update, context: CallbackContext) -> None:
    global data
    update.message.reply_text("尋車中...")

    while 1==1:
        r = requests.post('https://irentcar-app.azurefd.net/api/AnyRent', json={"ShowALL": "0", "Radius": search_radius_km, "Latitude": update.message.location.latitude, "Longitude": update.message.location.longitude})
        data = json.loads(r.text)
        count_car = sum(1 for line in data['Data']['AnyRentObj'])
        if count_car !=0:
            update.message.reply_text("目前附近可用車數: " + str(count_car))
            for itemm in (data['Data']['AnyRentObj']):
                car_distant =  haversine(float(itemm['Longitude']), float(itemm['Latitude']), float(update.message.location.longitude), float(update.message.location.latitude))
                update.message.reply_text('\n 車號: ' +  itemm['CarNo'] + '\n' + '距離 ' + str(round(float(car_distant)*1000)) + " 公尺遠" )
                my_params3 = {'chat_id': update.message.chat_id, 'latitude': itemm['Latitude'], 'longitude':itemm['Longitude']}
                r2 = requests.get('https://api.telegram.org/bot' + telegram_bot_token + '/sendlocation', params = my_params3)
            update.message.reply_text("尋車結束")
            break
        time.sleep(5)
        update.message.reply_text("測試中")
     


def search_address(update: Update, context: CallbackContext) -> None:
    global data
    update.message.reply_text("地址查詢與轉換經緯度中...")
    uuu = get_coordinate(update.message.text)
    update.message.reply_text("完補地址：" + uuu[2])

    my_params = {'chat_id': update.message.chat_id, 'latitude': uuu[0], 'longitude':uuu[1]}
    r2 = requests.get('https://api.telegram.org/bot' + telegram_bot_token + '/sendlocation', params = my_params)
    update.message.reply_text("尋車中...")

    while 1==1:
        r = requests.post('https://irentcar-app.azurefd.net/api/AnyRent', json={"ShowALL": "0", "Radius": search_radius_km, "Latitude": uuu[0], "Longitude": uuu[1]})   
        data = json.loads(r.text)
        count_car = sum(1 for line in data['Data']['AnyRentObj'])
        if count_car !=0:
            update.message.reply_text("目前附近可用車數: " + str(count_car))
            for itemm in (data['Data']['AnyRentObj']):
                car_distant =  haversine(float(itemm['Longitude']), float(itemm['Latitude']), float(uuu[1]), float(uuu[0]))
                update.message.reply_text('\n 車號: ' +  itemm['CarNo'] + '\n' + '距離 ' + str(round(float(car_distant)*1000)) + " 公尺遠" )
                my_params3 = {'chat_id': update.message.chat_id, 'latitude': itemm['Latitude'], 'longitude':itemm['Longitude']}
                r2 = requests.get('https://api.telegram.org/bot' + telegram_bot_token + '/sendlocation', params = my_params3)
            update.message.reply_text("尋車結束")
            break
        time.sleep(5)
        update.message.reply_text("測試中")


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)
    

# Functions


def get_coordinate(addr):
    browser = webdriver.Chrome("./chromedriver", options=options)
    browser.get("http://www.map.com.tw/")
    search = browser.find_element_by_id("searchWord")
    search.clear()
    search.send_keys(addr)
    browser.find_element_by_xpath("/html/body/form/div[10]/div[2]/img[2]").click() 
    time.sleep(2)
    iframe = browser.find_elements_by_tag_name("iframe")[1]
    browser.switch_to.frame(iframe)
    real_address = browser.find_element_by_xpath("/html/body/form/div[4]/table/tbody/tr[1]/td/table/tbody/tr[4]/td").text    
    coor_btn = browser.find_element_by_xpath("/html/body/form/div[4]/table/tbody/tr[3]/td/table/tbody/tr/td[2]")
    coor_btn.click()
    coor = browser.find_element_by_xpath("/html/body/form/div[5]/table/tbody/tr[2]/td")
    coor = coor.text.strip().split(" ")
    lat = coor[-1].split("：")[-1]
    log = coor[0].split("：")[-1]
    browser.quit()
    return (lat, log, real_address)




def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.

    global telegram_bot_token
    global search_radius_km

    telegram_bot_token = "<輸入你自己的從 telegram bot father 取得的 token>"
    search_radius_km = "1.5"

    updater = Updater(telegram_bot_token)


    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("address", search_address))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.location, search_location))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
