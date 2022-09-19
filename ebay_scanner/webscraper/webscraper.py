from logging import error
import requests
from bs4 import BeautifulSoup
from decimal import Decimal
from datetime import datetime
from page_generation.page_generator import GenerateHTML
from webscraper.item import EbayItem
import os.path
from notifications.notification import Notification

class Webscrapper:
    def __init__(self, url):
        self.url = url
        self.change = 0

    def clean_history(self, list):
        clean_list = []
        for item in list:
            clean_list.append(item.replace('\n',''))
        return clean_list
        
    # TODO: Implement Logging and Error handling so that if main block fails it Logs and Carries on running
    # TODO: Apply abstraction to the Scrape method 
    def scrape(self):
        history =  open('history.txt', 'r').readlines()
        self.now = datetime.now()
        res = requests.get(self.url)
        soup = BeautifulSoup(res.content, 'html.parser')
        item_count= 0
        potential_product_count = 0
        listings = soup.find_all("div", {"class": "s-item__wrapper clearfix"})
        items = []

        # Get each item on the Lowest Price + Buy it Now listings
        for product in listings:
            item_info = product.find("div", {"class": "s-item__info clearfix"})
            item_count != 1
            lower_info_text = item_info.text.lower()
            condition = ["in hand", "in-hand", "in - hand"]

            # Check the seller has advertised item is in hand
            if condition[0] in lower_info_text  or condition[1] in lower_info_text or condition[2] in lower_info_text:
                price = 0
                detail_items = item_info.find_all("div", {"class", "s-item__detailundefined s-item__detail--primary"})
                price = detail_items[0].find('span', {'class': 's-item__price'})
                if price != 0:
                    real_price = price.text.replace("£", "").replace("�", "").replace("$", "").replace("€", "").replace(',', '')
                    # TODO: Clean input to Float parsing below
                    # TODO: Make Target Price dynamic - possibly in config file 
                    if float(real_price.replace(",","")) <= 999:
                        item = EbayItem()
                        potential_product_count += 1
                        item_link = item_info.find('a', {'class': 's-item__link'}).attrs['href']
                        title = item_info.find('h3', {'class': 's-item__title'}).text.replace(',', '')
                        item.process_item_data(title, real_price, item_link)
                        print(item.get_item_data())
                        columns = item.get_item_data().split(',')
                        
                        if columns[0] not in self.clean_history(history):
                            print(columns[0])
                            print(history)
                            notification = Notification(item.get_item_data(),'7123456789') # MOBILE NUMBER FOR NOTIFICATION
                            with open('history.txt', 'a') as f:
                                f.write(columns[0]+'\n')
                                f.close()
                                
                            notification.send_sms_notification()
                            print('New item recoreded')

                        items.append(item.get_item_data())

        print(f"Total of {potential_product_count} potential products")
        print(f"Last refreshed at: {self.now}")
    # TODO: Implement code to generate HTML in var/www/html for history and current items
    #                 self.generate_pages_and_notify(items, current_change, potential_product_count)

    # def generate_pages_and_notify(self, items, current_change, potential_product_count):
    #     current_items = GenerateHTML('items.html')
    #     historic_items = GenerateHTML('items_archive.html')
            
    #     if self.change > current_change:
    #         print('--??!!Notification!!!??--')
    #         with open('history.txt', 'w') as f:
    #             for item in items:
    #                 f.write(item)
    #                 f.write('\n')

