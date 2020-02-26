# Hilleberg_Scraper
A scraper for the B-Ware Sale of the tent manufacturer Hilleberg.
This program is based on the wg_gesucht repository and compare the already existing items with new ones and notify via telegram or pushover (or both/none).

## Before use ##
Define your preferred way of notification in the config.txt file under use_notification and set your pushover user-token & app-token or your telegram bot-token & bot-chatID before use or there will be no notification. Also check the URL (main.py).


**config.txt**

![config](https://user-images.githubusercontent.com/55713049/71785761-c36da780-3003-11ea-99b2-eeb8a87aed50.png)


**URL (main.py)**

![url](https://user-images.githubusercontent.com/55713049/71785790-22332100-3004-11ea-82ed-b13ead70419b.png)


**ATTENTION** 

The scraper is using BeautifulSoup4, so you have to install it on your machine.

First install python3-pip with:

```
sudo apt-install python3-pip
```

And the Bs4-Modul with:
```
pip3 install bs4
```

## Extra Information ##
If deployed on a server or raspberry-pi use a crontab to let it run in the background.
A good interval would be every 5 minutes.

```
crontab -e
```
And insert following crontab statement:
```
*/5 * * * * cd /your/path/to/script/hilleberg_scraper && exec python3 main.py
```


**Things to know**
If you are interesting in changing the code take a look into the test.html file.
It shows you a small overview of the use html dataset.
