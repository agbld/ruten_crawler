#%%
import pandas as pd
import os
import uuid

from multiprocessing import Pool
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm

from utils import get_product_info

def worker_function(rows):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    product_infos = []
    try:
        for row in rows:
            cat_url, sub_cat_url, product_url = row
            product_info = get_product_info(product_url, driver)
            product_info['cat_url'] = cat_url
            product_info['sub_cat_url'] = sub_cat_url
            product_info['product_url'] = product_url
            product_infos.append(product_info)
    except Exception as e:
        print(f"Error processing rows: {e}")
    finally:
        driver.quit()

    # Check if the directory exists, if not, create it
    if not os.path.exists(".multiproc_tmp"):
        os.makedirs(".multiproc_tmp")

    # Save the results to a unique CSV file
    filename = f".multiproc_tmp/{uuid.uuid4().hex}.csv"
    product_infos_df = pd.DataFrame(product_infos)
    product_infos_df.to_csv(filename, index=False)

    return filename

if __name__ == '__main__':
    df = pd.read_csv('product_urls.csv')
    df = df.drop_duplicates(subset=['item_url'])

    # Split the DataFrame into chunks
    chunk_size = 15
    rows = [list(t) for t in zip(*[iter(df.itertuples(index=False, name=None))]*chunk_size)]

    with Pool(processes=12) as pool:
        results = list(tqdm(pool.imap(worker_function, rows), total=len(rows)))

    # Combine all the CSV files into one DataFrame
    product_infos_list = []
    for filename in results:
        if filename is not None:
            df = pd.read_csv(filename)
            product_infos_list.append(df)

    product_infos_df = pd.concat(product_infos_list)
    product_infos_df.to_csv('product_infos.csv', index=False)
    print('saved to product_infos.csv')



# %%
