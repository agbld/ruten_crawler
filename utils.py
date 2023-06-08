import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# get all sub-category urls from a specific category url
def get_sub_cat_urls(cat_url, driver):
    driver.get(cat_url)
    sub_cat_url_prefix = cat_url + '0'
    sub_cat_urls = []
    for url in driver.find_elements_by_tag_name('a'):
        href = url.get_attribute('href')
        if href and href.startswith(sub_cat_url_prefix):
            sub_cat_urls.append(href)
    return list(set(sub_cat_urls))

# get all product urls from a specific sub-category url and page index
def get_product_urls(sub_cat_url, driver, page_index=1):
    driver.get(f'{sub_cat_url}?p={page_index}')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href^='https://www.ruten.com.tw/item/show?']")))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    urls = []
    for url in driver.find_elements_by_tag_name('a'):
        href = url.get_attribute('href')
        if href and href.startswith('https://www.ruten.com.tw/item/show?'):
            urls.append(href)
    return urls

# get product info (product name, price, stock) from a specific product url
def get_product_info(product_url, driver):
    driver.get(product_url)    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href^='https://www.ruten.com.tw/item/show?']")))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    product_info = {}

    # product name
    product_info['prod_name'] = soup.find('meta', property='og:title')['content']
    
    # price (range)
    product_desc = soup.find('meta', property='og:description')['content']
    start_idx = product_desc.find('直購價: ')+5
    end_idx = product_desc.find(',', start_idx)
    product_info['price_str'] = product_desc[start_idx: end_idx].strip()
    
    # stock
    start_idx = product_desc.find('庫存: ')+3
    end_idx = product_desc.find(',', start_idx)
    product_info['stock'] = product_desc[start_idx: end_idx].strip()
    
    # TODO
    # 規格 & 項目
    # product_info['規格'] = []
    # product_info['項目'] = []
    # specs = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.item-purchase-content')))
    # for spec in specs:
    #     spec_name = spec.find_element(By.CSS_SELECTOR, 'li.item-spec-list-item').text
    #     options = ['']#spec.find_elements(By.CSS_SELECTOR, 'div.rt-store-goods-spec__style__spec-option')
    #     for option in options:
    #         if '規格' in spec_name:
    #             product_info['規格'].append(option.text.strip())
    #         elif '項目' in spec_name:
    #             product_info['項目'].append(option.text.strip())

    return product_info
                