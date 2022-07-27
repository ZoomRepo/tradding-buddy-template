import time
from threading import Thread
from webscraper.webscraper import Webscrapper

# TODO: Need to possibly add GUI for Webscrapper Service
class worker(Thread):
    def run(self):
        # TODO: Make it possible to instantiate multiple webscrapers for different items at different Prices time
        # TODO: Try to also write a script to gather Min/Max Buy and Sell Margins based on Completed Item sales on eBay
        # TODO: Add support for other Providers e.g. Amazon, find other online platforms to Buy/Sell
        scraper = Webscrapper("https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=bobcat+miner+300+inhand&_sacat=179171&LH_TitleDesc=0&LH_BIN=1&_sop=15")
        while(True):            
            scraper.scrape()
            time.sleep(5)

def run():
    worker().start()

run()
