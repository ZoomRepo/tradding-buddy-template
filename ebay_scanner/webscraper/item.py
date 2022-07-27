import json 

class EbayItem:
    def __init__(self):
        self.item_no = ""
        self.title = ""
        self.price = -1
        self.url = ""

    def extract_item_number(self, url):
        self.item_no = url.split('/itm/')[1].split('?')[0]

    def process_item_data(self, title, price, url):
        self.extract_item_number(url)
        self.title = title
        self.price = price
        self.url = url


    def get_item_data(self):
        csv_string = f'{self.item_no},{self.title},{self.price},{self.url}'
        return csv_string