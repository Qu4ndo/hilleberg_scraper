import configparser
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import csv
from push import send_push_message
from telegram import telegram_bot_sendtext

#CHANGE THIS URL!
myurl = "https://hilleberg.com/deu/zelt/outlet-zelt"


#read the config.txt
config = configparser.ConfigParser()
config.read_file(open(r'config.txt'))
use_notification = config.get('Basic-Configuration', 'use_notification')
use_notification = int(use_notification)
user_token = config.get('Pushover', 'user_token')
app_token = config.get('Pushover', 'app_token')
bot_token = config.get('Telegram', 'bot_token')
bot_chatID = config.get('Telegram', 'bot_chatID')


#read the html of the website
uClient = uReq(myurl)
page_html = uClient.read()
uClient.close()

#html parserTYmVs5iYk3T7kh
page_soup = soup(page_html, "html.parser")

#grabs each article
articles = page_soup.findAll("div", {"class":"buy"})

#list to test against
article_list = []

for article in articles:
    model = article.div.find("p", {"class":"model"}).get_text()
    color = article.div.find("p", {"class":"color"}).get_text()
    regular_price = article.div.find("p", {"class":"price"}).get_text()
    reduced_price = article.div.find("p", {"class":"outPrice"}).get_text()
    description = article.find("div", {"class":"buyBlock description"}).p.get_text()
    description = description.replace("\n", "").replace("\r", "")
    link = article.find("div", {"class":"buyBlock button"}).div.find("a", {"class":"cartLink"}).get("href")
    if model != "":
        article_list.append((model, color, regular_price, reduced_price, description))


#list of already found articles (csv)
found_list = []

#open csv with already listed articles
filename_buffer = "hilleberg.csv"
b = open(filename_buffer, "r+")
article_csv = csv.reader(b, delimiter=';')

for item in article_csv:
        found_list.append((item[0], item[1], item[2], item[3], item[4]))

b.close()

#overwrite the csv
filename_buffer = "hilleberg.csv"
b = open(filename_buffer, "w")

#list to add
add_list = []

#cycle through list and check
for article in article_list:
    if article in found_list:
        print("do nothing...")
    else:
        print(article)
        add_list.append(article)

        article = "Model: " + article[0] + " - " + article[1] + " / " + article[2] + " - " + article[3]
        if use_notification == 1:
            send_push_message(user_token, app_token, "New Tent found!", article)
        elif use_notification == 2:
            telegram_bot_sendtext(bot_token, bot_chatID, "New Tent found => " + article)
        elif use_notification == 3:
            send_push_message(user_token, app_token, "New Tent found!", article)
            telegram_bot_sendtext(bot_token, bot_chatID, "New Tent found => " + article)
        elif use_notification == 4:
            continue

#add already found articles to add_list
for item in found_list:
    add_list.append(item)

#add items to csv
for item in add_list:
    b.write(item[0] + ";" + item[1] + ";" + item[2] + ";" + item[3] + ";" + item[4] + "\n")

b.close()
