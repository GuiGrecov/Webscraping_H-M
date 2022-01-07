# ================================ IMPORTS =============================================
import requests
import pandas as pd
import numpy as np
import math
import pandas as pd
import re
import numpy as np


from IPython.display import Image
from datetime import datetime
from bs4 import BeautifulSoup

# ================================ FUNCTIONS ===========================================
def get_showroom_data(url, headers):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    # 1.0. Scrape data - Showroom products
    products = soup.find('ul', class_='products-listing small')
    product_list = products.find_all('article', class_='hm-product-item')

    # product id
    product_id = [p.get('data-articlecode') for p in product_list]

    # product category
    product_category = [p.get('data-category') for p in product_list]

    # product name
    product_list = products.find_all('a', class_='link')
    product_name = [p.get_text() for p in product_list]

    # price
    product_list = products.find_all('span', class_='price regular')
    product_price = [p.get_text() for p in product_list]

    data_scraped = pd.DataFrame([product_id, product_category, product_name, product_price]).T
    data_scraped.columns = ['product_id', 'product_category', 'product_name', 'product_price']

    # scrapy datetime
    data_scraped['scrapy_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # style_id
    data_scraped['style_id'] = data_scraped['product_id'].apply(lambda x: x[:-3])

    return data_scraped


def get_product_details(data_scraped):
    # 2.0. Scrape data - Products Details
    cols = ['Art. No.', 'Composition', 'Fit', 'Product safety', 'Size', 'More sustainable materials']
    df_pattern = pd.DataFrame(columns=cols)

    # unique columns for all products
    aux = []

    # Iterate over products
    df_raw = pd.DataFrame()

    for i in range(len(data_scraped)):
        url = 'https://www2.hm.com/en_us/productpage.' + data_scraped.loc[i, 'product_id'] + '.html'
        page = requests.get(url, headers=headers)

        # Beautiful Soup object
        soup = BeautifulSoup(page.text, 'html.parser')

        # ==================== color name =================================
        product_list = soup.find_all('a', class_='filter-option miniature') + soup.find_all('a',
                                                                                            class_='filter-option miniature active')
        color_name = [p.get('data-color') for p in product_list]

        # product id
        product_id = [p.get('data-articlecode') for p in product_list]

        df_color = pd.DataFrame([product_id, color_name]).T
        df_color.columns = ['product_id', 'color_name']

        # ==================== Iterate over colors =================================
        df_details_composition = pd.DataFrame()
        for j in range(len(df_color)):
            url = 'https://www2.hm.com/en_us/productpage.' + str(df_color.loc[j, 'product_id']) + '.html'
            page = requests.get(url, headers=headers)

            # Beautiful Soup object
            soup = BeautifulSoup(page.text, 'html.parser')

            # ==================== composition =================================
            product_composition_list = soup.find_all('div', class_='pdp-description-list-item')
            product_composition = [list(filter(None, p.get_text().split('\n'))) for p in product_composition_list]

            # reaname dataframe
            df_composition = pd.DataFrame(product_composition).T
            df_composition.columns = df_composition.iloc[0]

            # delete first row
            df_composition = df_composition.iloc[1:].fillna(method='ffill')

            # garantee the same number of columns
            df_composition = pd.concat([df_pattern, df_composition], axis=0)

            # generate style id + color id
            df_composition['product_id'] = df_composition['Art. No.']
            df_composition['color_id'] = df_composition['Art. No.'].apply(lambda x: x[-3:])

            # ==================== price + product_id =================================
            df_composition['product_price'] = soup.find_all('span', class_='price-value')[0].get_text()
            df_composition['product_name'] = soup.find_all('h1', class_='primary product-item-headline')[0].get_text()

            aux = aux + df_composition.columns.tolist()

            # all products composition
            df_details_composition = pd.concat([df_details_composition, df_composition], axis=0)

        df_details = pd.merge(df_color, df_details_composition.drop_duplicates(), how='left', on='product_id')
        df_details['style_id'] = df_details['product_id'].apply(lambda x: x[:-3])

        # join with showroom
        data_aux = pd.merge(df_details,
                            pd.DataFrame(data_scraped.loc[i, ['style_id', 'product_category', 'scrapy_datetime']]).T,
                            how='left', on='style_id')

        # final dataset
        df_raw = pd.concat([df_raw, data_aux], axis=0)

    return df_raw


def datacleaning(data):
    # product id
    data = data.dropna(subset=["product_id"])
    # data transformertion -> data["product_id"] = data["product_id"].astype(int)

    # product name
    data['product_name'] = data['product_name'].apply(lambda x: x.replace(' ', '_').lower())
    data['product_name'] = data['product_name'].apply(lambda x: x.replace('\t', '').lower())
    data['product_name'] = data['product_name'].apply(lambda x: x.replace('\n__', '').lower())

    # product price
    data["product_price"] = data["product_price"].apply(lambda x: x.replace("$", "")).astype(float)

    # color name
    data["color_name"] = data["color_name"].apply(lambda x: x.replace(" ", "_").lower() if pd.notnull(x) else x)

    # fit
    data["Fit"] = data["Fit"].apply(lambda x: x.replace(" ", "_").lower() if pd.notnull(x) else x)

    # size model
    data["size_model"] = data["Size"].str.extract("(\d+/\\d+)")

    # size number
    data["size_number"] = data["Size"].apply(lambda x: re.search("\d{3}cm", x).group(0) if pd.notnull(x) else x)
    data["size_number"] = data["size_number"].apply(lambda x: re.search("\d+", x).group(0) if pd.notnull(x) else x)

    # dropna Size
    data = data.drop(columns=["Size"], axis=1)

    # product safety
    data = data.drop(columns=["Product safety"], axis=1)

    # composition
    data = data[~data["Composition"].str.contains("Pocket lining: ", na=False)]
    data = data[~data["Composition"].str.contains("Lining: ", na=False)]
    data = data[~data["Composition"].str.contains("Shell: ", na=False)]

    # reset index
    data = data.reset_index(drop=True)

    # break composition by comma
    df1 = data["Composition"].str.split(",", expand=True)

    # cotton | polyester | elastano | elasterell
    df_ref = pd.DataFrame(index=np.arange(len(data)), columns=["cotton", "polyester", "spandex", "elasterell"])

    # cotton
    df_cotton = df1[0]
    df_cotton.name = "cotton"
    df_ref = pd.concat([df_ref, df_cotton], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated(keep="last")]

    # polyester
    df_poly = df1.loc[df1[1].str.contains("Polyester", na=True), 1]
    df_poly.name = "polyester"
    df_ref = pd.concat([df_ref, df_poly], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated(keep="last")]

    # elastano
    df_elastane = df1.loc[df1[1].str.contains("Spandex", na=True), 1]
    df_elastane.name = "spandex"
    # combine elastane from both columns
    df_elastane = df_elastane.combine_first(df1[2])

    # combine elastane from both columns
    # df_elastane = df_elastane.combine_first(df1[2])

    df_ref = pd.concat([df_ref, df_elastane], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated(keep="last")]

    # elasterell
    df_el = df1.loc[df1[1].str.contains("Elasterell", na=True), 1]
    df_el.name = "elasterell"
    df_ref = pd.concat([df_ref, df_el], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated(keep="last")]

    # data
    data = pd.concat([data, df_ref], axis=1)
    data = data.iloc[:, ~data.columns.duplicated(keep="last")]
    data.head()

    # format composition data
    data["cotton"] = data["cotton"].apply(lambda x: int(re.search("\d+", x).group(0)) / 100 if pd.notnull(x) else x)
    data["polyester"] = data["polyester"].apply(
        lambda x: int(re.search("\d+", x).group(0)) / 100 if pd.notnull(x) else x)
    data["spandex"] = data["spandex"].apply(lambda x: int(re.search("\d+", x).group(0)) / 100 if pd.notnull(x) else x)
    data["elasterell"] = data["elasterell"].apply(
        lambda x: int(re.search("\d+", x).group(0)) / 100 if pd.notnull(x) else x)

    # product safety
    data = data.drop(columns=["Composition"], axis=1)

    return data


def export(data, name):
    # export archive to csv

    # code = archive today
    code = str(datetime.today().strftime('%Y-%m-%d'))

    # var responsible to generate the archive of today
    name = name + code + ".csv"

    # ajuste data
    data = data.drop_duplicates(subset=['product_id', 'product_category', 'product_name', 'product_price',
                                        'scrapy_datetime', 'style_id', 'color_id', 'color_name', 'Fit'], keep="last")

    data.shape

    # =====export data========
    data.to_csv(name, encoding="utf-8", index=False)


#=========== MAIN CODE =================

if __name__ == "__main__":
    # parameters
    url = 'https://www2.hm.com/en_us/men/products/jeans.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) , AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

    # Extraction
    data_scraped = get_showroom_data(url, headers)

    # Transformation
    df_raw = get_product_details(data_scraped)

    # Carga
    data = datacleaning(df_raw)

    # export to csv in local notebook
    export(data, "H&M - Datas/products-clean")

