import pandas as pd
from selenium import webdriver
import glob
import os
from tqdm import tqdm
import re
import argparse

#BaseLines.py C:\Users\Walid\Desktop\Selenium\geckodriver.exe df_annotated_cleaned.xlsx


def firs_baseline(df_annotated_clean, geckodriver_path=r'C:\Users\Walid\Desktop\Selenium\geckodriver.exe'):
    description_missing = 0
    price_missing = 0
    out = []
    driver = webdriver.Firefox(executable_path=geckodriver_path)
    
    for i in tqdm(range(df_annotated_clean.shape[0])):
        url_local = df_annotated_clean['URL_Local'][i]
        driver.get(os.getcwd()+'\\'+url_local)

        title = driver.title
        try:
            description = driver.find_element_by_xpath("//*[@name='description']").get_attribute("content")
        except:
            description_missing += 1
            description = ""
        element_price = driver.find_elements_by_xpath("//*[contains(@property,'price')]")
        for element in element_price:
            try :
                price = float(element.replace(',','.'))
                break
            except:
                price =""
                price_missing+=1
                
        
        out.append([url_local, df_annotated_clean['URL_Live'][i], df_annotated_clean['URL_Parent'][i], title, description, price])
        
    df_out = pd.DataFrame(out, columns=['URL_Local','URL_Live','URL_Parent','Title_Content','Description_Content','Price_content'])
    df_out.to_excel('First_Baseline.xlsx', index=False)
    driver.close()
    return df_out, df_annotated_clean.shape[0], '{:.1%}'.format(1), '{:.1%}'.format(1-description_missing/df_annotated_clean.shape[0]), '{:.1%}'.format(1-price_missing/df_annotated_clean.shape[0])



def second_baseline(df_annotated_clean, geckodriver_path=r'C:\Users\Walid\Desktop\Selenium\geckodriver.exe'):
    price_missing = 0
    title_missing = 0
    out = []
    driver = webdriver.Firefox(executable_path=geckodriver_path)
    
    for i in tqdm(range(df_annotated_clean.shape[0])):
        url_local = df_annotated_clean['URL_Local'][i]
        driver.get(os.getcwd()+'\\'+url_local)
        
        title_elements = driver.find_elements_by_tag_name("h1")
        title_txt = ""
        for element in title_elements:
            if len(element.text) > 0 :
                title_txt = element.text
            break
        
        price_elements = driver.find_elements_by_xpath("//*[contains(@class,'price')]")
        price = ""
        for element in price_elements:
            price_txt = element.text
            numbers = re.findall(r"[-+]?\d*\.\d+|\d+ ", price_txt.replace(',','.'))
            if numbers!=[]:
                price = numbers[0]
                break
        out.append([url_local, df_annotated_clean['URL_Live'][i], df_annotated_clean['URL_Parent'][i], title_txt, price])
        
    df_out = pd.DataFrame(out, columns=['URL_Local','URL_Live','URL_Parent','Title_Content','Price_content'])
    df_out.to_excel('Second_Baseline.xlsx', index=False)
    driver.close()
    return df_out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path_geckodriver", help="Path to the firefox driver")
    parser.add_argument("path_df_annotated_clean", help="Path the df_annotated_cleaned")
    args = parser.parse_args()
    
    geckodriver_path = args.path_geckodriver
    df_annotated_clean = pd.read_excel(args.path_df_annotated_clean)
    
    
    firs_baseline(df_annotated_clean, geckodriver_path=geckodriver_path)
    second_baseline(df_annotated_clean, geckodriver_path=geckodriver_path)
    

if __name__ == "__main__":
    main()