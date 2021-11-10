# webProducts.py - Obtendo produtos do Mercado Livre a partir de uma busca realizada pelo user
# importante observar o padrão da URL

import requests
from bs4 import BeautifulSoup
import pandas as pd

products_list = []

url_base = 'https://lista.mercadolivre.com.br/'
product_name = str(input('Which product do you want? '))

res = requests.get(url_base + product_name)

try:
    res.raise_for_status()
except Exception as e:
    print('There was a problem: %s' % e)

site = BeautifulSoup(res.text, 'html.parser')

products = site.findAll('div', attrs={'class': 'andes-card andes-card--flat andes-card--default ui-search-result '
                                               'ui-search-result--core andes-card--padding-default'})

for product in products:
    product_title = product.find('h2', attrs={'class': 'ui-search-item__title'})
    product_link = product.find('a', attrs={'class': 'ui-search-link'})

    product_price = product.find('span', {'class': 'price-tag-fraction'})
    product_price_decimal = product.find('span', {'class': 'price-tag-cents'})

    if product_price_decimal:
        products_list.append([product_title.text, 'R$' + product_price.text + ',' + product_price_decimal.text,
                              product_link['href']])
    else:
        products_list.append([product_title.text, product_price, product_link['href']])

table = pd.DataFrame(products_list, columns=['Título', 'Preço', 'Link'])

table.to_excel('products.xlsx', index=False)
