#%%
# import
import pandas as pd

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from utils import get_sub_cat_urls

#%%
# get sub-cat urls
if __name__ == '__main__':
    sub_cat_url_prefix = 'https://www.ruten.com.tw/category/00'

    cat_indices = list(range(1, 16)) + list(range(17, 25)) # without 0025, which is 18+ content required additional actions

    sub_cat_urls_list = []
    sub_cat_urls_df = None

    driver = webdriver.Chrome(ChromeDriverManager().install())

    print('num of cat: ', len(cat_indices))
    for cat_index in cat_indices:
        f_cat_index = "{:02d}".format(cat_index)
        cat_url = f"{sub_cat_url_prefix}{f_cat_index}"
        print('working on cat: ', cat_url)
        
        sub_cat_urls = get_sub_cat_urls(cat_url, driver)
        
        print('num of sub-cat: ', len(sub_cat_urls))
        
        for sub_cat_url in sub_cat_urls:    # [:1] for debug
            print('working on sub-cat: ', sub_cat_url)
            sub_cat_urls_list.append({'cat_url': cat_url, 'sub_cat_url': sub_cat_url})

        sub_cat_urls_df = pd.DataFrame(sub_cat_urls_list)
        sub_cat_urls_df.to_csv('sub_cat_urls.csv', index=False)

    driver.close()
                
#%%
