#%%
# import
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

#%%
# functions

def get_sub_cat_urls(cat_url, driver):
    driver.get(cat_url)
    sub_cat_url_prefix = cat_url[:cat_url.rfind('/')]
    sub_cat_urls = []
    for url in driver.find_elements_by_tag_name('a'):
        href = url.get_attribute('href')
        if href and href.startswith(sub_cat_url_prefix):
            sub_cat_urls.append(href)
    return list(set(sub_cat_urls))

def get_product_urls(sub_cat_url, driver):
    driver.get(sub_cat_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href^='https://www.ruten.com.tw/item/show?']")))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    urls = []
    for url in driver.find_elements_by_tag_name('a'):
        href = url.get_attribute('href')
        if href and href.startswith('https://www.ruten.com.tw/item/show?'):
            urls.append(href)
    return urls

# TODO
def get_product_info_legacy(product_url, driver):
    driver.get(product_url)    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href^='https://www.ruten.com.tw/item/show?']")))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    product_info = {}

    # 商品名稱
    product_info['商品名稱'] = soup.find('meta', property='og:title')['content']
    
    
    # 直購價
    product_desc = soup.find('meta', property='og:description')['content']
    start_idx = product_desc.find('直購價: ')+5
    end_idx = product_desc.find(',', start_idx)
    product_info['直購價'] = product_desc[start_idx: end_idx].strip()
    
    # 數量
    start_idx = product_desc.find('庫存: ')+3
    end_idx = product_desc.find(',', start_idx)
    product_info['數量'] = product_desc[start_idx: end_idx].strip()
    
    # 規格 & 項目
    product_info['規格'] = []
    product_info['項目'] = []
    specs = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.item-purchase-content')))
    for spec in specs:
        spec_name = spec.find_element(By.CSS_SELECTOR, 'li.item-spec-list-item').text
        options = ['']#spec.find_elements(By.CSS_SELECTOR, 'div.rt-store-goods-spec__style__spec-option')
        for option in options:
            if '規格' in spec_name:
                product_info['規格'].append(option.text.strip())
            elif '項目' in spec_name:
                product_info['項目'].append(option.text.strip())

    # url
    product_info['url'] = product_url

    return product_info

# TODO
def get_product_info(url, driver):
    driver.get(url)
    driver.implicitly_wait(6)

    #商品名稱
    product = driver.find_element(By.XPATH,'//*[@id="main-layout"]/div/div[2]/h1/span')
    product_text = product.text
    # print(product_text)

    #價錢
    prices = driver.find_element(By.XPATH,'//*[@id="main_form"]/div[1]/strong')
    prices_text = prices.text
    # print(prices_text)

    #抓取庫存數
    stock = driver.find_element(By.XPATH,'//*[@id="main_form"]/div[2]/div/div[2]/div/div/span')
    stock_text = stock.text
    # print(stock_text)

    #抓取規格
    for i in range(1,3):
        quantity_element = driver.find_element(By.XPATH,'//*[@id="main_form"]/div[2]/div/div[1]/div/ul/li['+ str(i) +']/label')
        quantity_element_text = quantity_element.text
        # print(quantity_element_text)
        
    return {'商品名稱':product_text,'價錢':prices_text,'庫存':stock_text,'規格':quantity_element_text}

#%%
# full crawl
if __name__ == '__main__':
    sub_cat_url_prefix = 'https://www.ruten.com.tw/category/00'
    cat_indices = [10]   # [10] for debug
    
    driver = webdriver.Chrome(ChromeDriverManager().install())

    print('num of cat: ', len(cat_indices))
    for cat_index in cat_indices:
        f_cat_index = "{:02d}".format(cat_index)
        cat_url = f"{sub_cat_url_prefix}{f_cat_index}"
        print('working on cat: ', cat_url)
        
        sub_cat_urls = get_sub_cat_urls(cat_url, driver)
        print('num of sub-cat: ', len(sub_cat_urls))
        
        for sub_cat_url in sub_cat_urls[:1]:    # [:1] for debug
            print('working on sub-cat: ', sub_cat_url)
        
            for page_index in range(1, 2):      # range(1, 2) for debug
                sub_cat_url = f"{sub_cat_url}?p={page_index}"
                item_urls = get_product_urls(sub_cat_url, driver)
                print(f'num of items in page {page_index} in sub-cat: ', len(item_urls))
                
                for item_url in item_urls[:1]:  # [:1] for debug
                    product_info = get_product_info(item_url, driver)
                    print(product_info)
                
#%%
