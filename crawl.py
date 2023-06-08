#%%
# import
import pandas as pd

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm

from utils import get_product_info

#%%
# get product infos
if __name__ == '__main__':
    df = pd.read_csv('product_urls.csv')
    df = df.drop_duplicates(subset=['item_url'])

    product_infos_list = []
    product_infos_df = None

    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    with tqdm(total=len(df)) as pbar:
        for _, row in df.iterrows():    # [:1] for debug
            cat_url = row['cat_url']
            sub_cat_url = row['sub_cat_url']
            product_url = row['item_url']
            
            try:
                product_info = get_product_info(product_url, driver)
            except:
                print('error: ', product_url)
                pbar.update(1)
                continue
            product_info['cat_url'] = cat_url
            product_info['sub_cat_url'] = sub_cat_url
            product_info['product_url'] = product_url
            
            # print(product_info)
            product_infos_list.append(product_info)
            
            # if _ % 20 == 0:
            #     product_infos_df = pd.DataFrame(product_infos_list)
            #     product_infos_df.to_csv('product_infos.csv', index=False)
            
            pbar.update(1)

    product_infos_df = pd.DataFrame(product_infos_list)
    product_infos_df.to_csv('product_infos.csv', index=False)


#%%