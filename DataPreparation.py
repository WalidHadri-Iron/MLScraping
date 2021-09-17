import pandas as pd
from selenium import webdriver
import glob
import os
from tqdm import tqdm
import argparse

#DataPreparation.py C:\Users\Walid\Desktop\Selenium\geckodriver.exe df_annotated.xlsx C:\Users\Walid\Desktop\Projet\pagess

def link_pages_dataframe(df_annotated, path_to_pages):
    """
    This function is to add in the initinal df_annotated the column with the reference to the local html pages.
    """
    urls = []
    for name in glob.glob(path_to_pages+'/*.html'):
        urls.append(name)
    urls.sort(key=lambda x:int(x.split('\\')[-1].split('.')[0]))
    df_annotated['URL_Local'] = urls
    return df_annotated

def extraction_verification(row_data_annotated, driver, display=True):
    """
    This function aims to verify that the annotation and web page downloading are good
    Takes in:
        row_data_annotated: one row from the annotated data (pandas row)
        driver: Selenium driver
        display: printing the results in consolse (boolean)
    """
    url_local = row_data_annotated['URL_Local']
    url_live = row_data_annotated['URL_Live']
    title_cssselector = row_data_annotated['Title']
    description_cssselector = row_data_annotated['Description']
    price_cssselector = row_data_annotated['Price']
    
    driver.get(url_local)
    
    if not pd.isna(title_cssselector):
        title = driver.find_element_by_css_selector(title_cssselector).text
    else:
        title = "Not Found"
    if not pd.isna(description_cssselector):
        description = driver.find_element_by_css_selector(description_cssselector).text
    else:
        description = "Not Found"
    if not pd.isna(price_cssselector):
        price = driver.find_element_by_css_selector(price_cssselector).text
    else:
        price = "Not Found"
    
    if display:
        print('-------------------', url_live, '----------------------------')
        print('------------------', url_local, '----------------------------')
        print('Title: ', title)
        print('--------------------------------------------')
        print('Decription:', description)
        print('--------------------------------------------')
        print("Price :", price)
    
        
    return url_local, url_live, row_data_annotated['URL_Parent'], title, description, price

def extraction_verification_all(df_annotated, geckodriver_path=r'C:\Users\Walid\Desktop\Selenium\geckodriver.exe'):
    driver = webdriver.Firefox(executable_path=geckodriver_path)
    out = []
    indices_to_delete = []
    for i in tqdm(range(df_annotated.shape[0])):
        try:
            row_data_annotated = df_annotated.iloc[i]
            out.append(extraction_verification(row_data_annotated, driver, display=False))
        except:
            print('-------------------',i,'---------------')
            indices_to_delete.append(i)
    driver.close()
    df_verification = pd.DataFrame(out, columns=['URL_Local','URL_Live','URL_Parent','Title_Content','Description_Content','Price_Content'])
    bad_indices = df_annotated.index.isin(indices_to_delete)
    df_annotated_new = df_annotated[~bad_indices]
    df_annotated_new.reset_index(inplace=True, drop=True)
    df_annotated_new.to_excel('df_annotated_cleaned.xlsx', index=False)
    df_verification.to_excel('df_verification.xlsx', index=False)
    return out

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path_geckodriver", help="Path to the firefox driver")
    parser.add_argument("path_df_annotated", help="Path the df_annotated")
    parser.add_argument("path_folder_pages", help="Path the folder pages")
    args = parser.parse_args()
    
    geckodriver_path = args.path_geckodriver
    df_annotated = pd.read_excel(args.path_df_annotated)
    path_to_pages = args.path_folder_pages
    
    df_annotated = link_pages_dataframe(df_annotated, path_to_pages)
    extraction_verification_all(df_annotated, geckodriver_path=geckodriver_path)

if __name__ == "__main__":
    main()