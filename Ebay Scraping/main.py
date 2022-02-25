from selenium import webdriver
import os
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd

path = os.getcwd()
driver_path = '{}\chromedriver.exe'.format(path)
driver = webdriver.Chrome(driver_path)
driver.get('https://www.ebay.com/')

article_to_search = 'Computadora'
article = driver.find_element_by_xpath('//input[@placeholder="Buscar artículos"]')
article.send_keys(article_to_search)

send = driver.find_element_by_xpath('//input[@value="Buscar"]')
send.click()
time.sleep(2)

all_names = []
all_prices = []
all_urls = []

for i in range(4):
    
    # Get all products names
    product_names = driver.find_elements_by_xpath('//ul[@class="srp-results srp-list clearfix"]/li//h3[@class="s-item__title"]')
    names = [i.text for i in product_names]
    all_names.extend(names)
    
    #Get all products prices
    prices = driver.find_elements_by_xpath('//ul[@class="srp-results srp-list clearfix"]/li//div[@class="s-item__info clearfix"]//div[@class="s-item__details clearfix"]/div[1]/span')
    price = [i.text for i in prices]
    all_prices.extend(price)
    
    #Get products urls
    urls = driver.find_elements_by_xpath('//ul[@class="srp-results srp-list clearfix"]/li//div[@class="s-item__info clearfix"]//a[@class="s-item__link"]')
    url = [i.get_attribute('href') for i in urls]
    all_urls.extend(url)
    
    try:
        next_page = driver.find_element_by_xpath('//a[@class==pagination__next icon-link]')
        next_page.click()
    except:
        break

df = pd.DataFrame({"productos": all_names,"precios": all_prices, "urls": all_urls})
df.to_csv('ebay_scraping.csv')        