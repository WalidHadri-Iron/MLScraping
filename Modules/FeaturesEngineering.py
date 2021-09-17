import pandas as pd
from selenium import webdriver
import os
from tqdm import tqdm
import argparse



#FeaturesEngineering.py C:\Users\Walid\Desktop\Selenium\geckodriver.exe df_annotated_cleaned.xlsx

def get_css_features(index_row, row_data_annotated, list_features_css, driver):
    """
    Get CSS values for given feature for the title, description and price
    Takes in:
    index_row: index of the row of the annotated data (pandas row)
    row_data_annotated: one row from the annotated data (pandas row)
    list_features_css: list of css features to consider (see https://docs.w3cub.com/css)
    driver: selenium driver
    """
    url_local = row_data_annotated.get('URL_Local', None)
    
    title_cssselector = row_data_annotated.get('Title', None)
    description_cssselector = row_data_annotated.get('Description', None)
    price_cssselector = row_data_annotated.get('Price', None)
    
    driver.get(os.getcwd()+'\\'+url_local)
    
    try:  
        title = driver.find_element_by_css_selector(title_cssselector)
        title_value = driver.find_element_by_css_selector(title_cssselector).text
    except:
        print('Unable to find title for row : {}'.format(index_row))
        title = None
        title_value = None
    
    try:
        description = driver.find_element_by_css_selector(description_cssselector)
        description_value = driver.find_element_by_css_selector(description_cssselector).text
    except:
        print('Unable to find description for row : {}'.format(index_row))
        description = None
        description_value = None
    
    try:
        price = driver.find_element_by_css_selector(price_cssselector)
        price_value = driver.find_element_by_css_selector(price_cssselector).text
    except:
        print('Unable to find price for row : {}'.format(index_row))
        price = None
        price_value = None
    
    elements = [title, description, price]
    dict_elemnts = {title: 'title', description: 'description', price: 'price'}
    
    features = dict()
    for element in [e for e in elements if e is not None]:
        styleprops_dict = driver.execute_script('var items = {};'+
                                       'var compsty = getComputedStyle(arguments[0]);'+
                                        'var len = compsty.length;'+
                                        'for (index = 0; index < len; index++)'+
                                        '{items [compsty[index]] = compsty.getPropertyValue(compsty[index])};'+
                                        'return items;', element)
        for feature_name in list_features_css:
            feature = styleprops_dict[feature_name]
            features[f'{dict_elemnts[element]}_{feature_name}'] = feature

    return title_value, description_value, price_value, features


def generate_features_css(df_annotated ,list_features_css, driver):
    """
    Generate pandas dataframe containing rows representing elements of the HTML page with their values and related features
    Takes in:
    df_annotated: pandas dataframe containing CSS selectors of the three caracteristics for a URL product page 
    list_features_css: css feature (see https://docs.w3cub.com/css)
    driver: selenium driver

    """
    rows_list = []
    for index, row in df_annotated.iterrows():  
        dict_title = {}
        dict_desc = {}
        dict_price = {}
        
        title_cssselector = row.get('Title', None)
        description_cssselector = row.get('Description', None)
        price_cssselector = row.get('Price', None)
        
        
        title_value, description_value, price_value, features = get_css_features(index, row, list_features_css, driver)
        
        dict_title['value'] = title_value
        dict_desc['value'] = description_value
        dict_price['value'] = price_value
        
        for feature_name in list_features_css:
            dict_title[feature_name] = features.get(f'title_{feature_name}', None)
            dict_desc[feature_name] = features.get(f'description_{feature_name}', None)
            dict_price[feature_name] = features.get(f'price_{feature_name}', None)
        
        dict_title["class"] = "title"
        dict_desc["class"] = "description"
        dict_price["class"] = "price"
        
        rows_list.append(dict_title)
        rows_list.append(dict_desc)
        rows_list.append(dict_price)

        print('Done for row : {} & page : {}'.format(index, index + 1))

    df = pd.DataFrame(rows_list)
    return df


def contains(value, to_find):
    """
    check if value of characteristic contains a number
    takes in:
    value : string of characteristic
    """
    if value is not None:
        return int(any(c in value for c in to_find))
    else:
        return 0
    
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path_geckodriver", help="Path to the firefox driver")
    parser.add_argument("path_df_annotated_cleaned", help="Path the df_annotated")
    args = parser.parse_args()
    
    geckodriver_path = args.path_geckodriver
    df_annotated_cleaned = pd.read_excel(args.path_df_annotated_cleaned)
    
    driver = webdriver.Firefox(executable_path=geckodriver_path)
    
    df_featured = generate_features_css(df_annotated_cleaned, ['font-size', 'font-style', 'font-stretch', 'font-weight', 'line-height', 'font-family', 'font-variant'], driver)   
    df_featured['length_value'] = df_featured['value'].apply(lambda value: len(value) if value is not None else 0)
    df_featured['contains_number'] = df_featured['value'].apply(lambda value: contains(value, to_find="0123456789"))
    df_featured['contains_currency'] = df_featured['value'].apply(lambda value: contains(value, to_find="¥$€£"))
    df_featured['contains_symbols'] = df_featured['value'].apply(lambda value: contains(value, to_find="?!.,:"))
    df_featured.to_csv('df_featured.csv', index=False)
    driver.close()
if __name__ == "__main__":
    main()