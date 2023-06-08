#%%
# import
import pandas as pd

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from utils import get_product_urls

#%%
# get product urls
if __name__ == '__main__':
    driver = webdriver.Chrome(ChromeDriverManager().install())

    sub_cat_urls_df = pd.read_csv('sub_cat_urls.csv')

    product_urls_list = []
    product_urls_df = None
    
    for _, row in sub_cat_urls_df.iterrows():    # [:1] for debug
        cat_url = row['cat_url']
        sub_cat_url = row['sub_cat_url']
        
        for page_index in range(1, 2):      # range(1, 2) for debug
            item_urls = get_product_urls(sub_cat_url, driver, page_index)
            print(f'num of items in page {page_index} in sub-cat: ', len(item_urls))
            
            for item_url in item_urls:  # [:1] for debug
                product_urls_list.append({'cat_url': cat_url, 'sub_cat_url': sub_cat_url, 'item_url': item_url})
            
        product_urls_df = pd.DataFrame(product_urls_list)
        product_urls_df.to_csv('product_urls.csv', index=False)

    driver.close()
                
#%%
