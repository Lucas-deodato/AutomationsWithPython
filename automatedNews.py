# news.py - script que gera uma planilha com as notícias na página inicial do site g1.globo

from bs4 import BeautifulSoup
import requests as req
import pandas as pd

news_list = []

res = req.get('https://g1.globo.com/')

content = res.content

site = BeautifulSoup(content, 'html.parser')

news = site.findAll('div', attrs={'class': 'feed-post-body'})  #

# percorre pelo "array(ResultSet)" que é retornado pelo findAll()
for new in news:
    # find() retorna a primeira ocorrência, porém com o loop, ele irá buscar as próximas também
    title = new.find('a', attrs={'class': 'feed-post-link'})

    new_time = new.find('span', attrs={'class': 'feed-post-datetime'})

    # verifica se existe o horário da postagem da notícia
    if new_time:
        news_list.append([title.text, new_time.text, title['href']])
    else:
        news_list.append([title.text, '', title['href']])

# cria uma tabela com os itens da lista, separando-os em 3 colunas
news_table = pd.DataFrame(news_list, columns=['Título', 'Horas', 'Link'])

# salva o arquivo no formato de arquivo recebido no excel; False = não salva os index
news_table.to_excel('news.xlsx', index=False)

print(news_table)
