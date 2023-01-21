# Import Package
import os
import csv
import re
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

# webdriver setup
opt = {#'head': '--headless',   #Not showing web browser UI
       'sandbox': '--no-sandbox',  # Bypass OS security model
       'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'
       }
option = Options()
for i in opt:
    option.add_argument(opt[i])

# Scraping
scraper = webdriver.Firefox(executable_path='C:/geckodriver-v0.31.0-win64/geckodriver.exe', options=option)
scraper.get('https://www.etsy.com/search?q=gift%20for%20women')
scraper.implicitly_wait(20)
result = scraper.find_elements(By.CSS_SELECTOR, 'ol.wt-grid.wt-grid--block.wt-pl-xs-0.tab-reorder-container > li')

data = {'url': '', 'title': '', 'price': '', 'sales': ''}
res = []

for i in result:
    try:
        data['url'] = i.find_element(By.CSS_SELECTOR, 'a.listing-link.wt-display-inline-block').get_attribute('href')
    except TypeError:
        break
    data['title'] = i.find_element(By.CSS_SELECTOR, 'h3.wt-text-caption.v2-listing-card__title').text
    data['title'] = re.sub(r'\n +', '', data['title'])
    data['price'] = i.find_element(By.CSS_SELECTOR,
                                   'div.n-listing-card__price.wt-display-flex-xs.wt-align-items-center > p.wt-text-title-01.lc-price > span:nth-of-type(2)').text
    data['price'] = re.sub(r'\D', '', data['price'])
    try:
        data['sales'] = i.find_element(By.CSS_SELECTOR,
                                       'span.wt-text-caption.wt-text-gray.wt-display-inline-block.wt-nudge-l-3.wt-pr-xs-1').text
        data['sales'] = re.sub(r'\D', '', data['sales'])
    except (AttributeError,NoSuchElementException) as e:
        data['sales'] = 0
    res.append(data.copy())

scraper.quit()

print(res)
print(f'\n{len(result)} products collected by selenium')

# save into csv file
filepath = 'C:/NaruProject/etsynium/result_sel.csv'
print('Creating file...')
folder = filepath.rsplit("/", 1)[0]
try:
    os.mkdir(folder)
except FileExistsError:
    pass
with open(filepath, 'w+', encoding="utf-8", newline='') as f:
    headers = ['url', 'title', 'price', 'sales']
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    for i in res:
        writer.writerow(i)
    f.close()
print(f'{filepath} created')