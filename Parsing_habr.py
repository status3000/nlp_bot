from bs4 import BeautifulSoup
import requests
import re



def parser(q, max_num):
    def clean_and_lemmatize(text):
        #cleaning
        text = re.sub(r'(\<(/?[^>]+)>)', '', text)
        return text
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0', 'Accept': '*/*', 'Accept-Encoding': '*', 'Accept-Language': '*', 'Connection': 'keep-alive'}
    foto_url = f"https://habr.com/ru/search/?q={q}&order=date"
    fotolist = requests.get(foto_url)
    a = BeautifulSoup(fotolist.text, 'html.parser')
    all_pages = a.find_all('a', attrs = {'class' : 'tm-article-snippet__title-link'})[:max_num]
   
    news_links = []
    articles = []
    for i in all_pages:
        news_links.append(str('https://habr.com' + str(i.get_attribute_list('href')[0])))
    for i in range(len(news_links)):    
        song_url = news_links[i]
        song_page = requests.get(song_url)
        song_html = BeautifulSoup(song_page.text, 'html.parser')
        t = song_html.find_all('div', attrs = {'xmlns' : 'http://www.w3.org/1999/xhtml'})
#         print(clean_and_lemmatize(''.join([str(i) for i in t])))
        articles.append(clean_and_lemmatize(''.join([str(i) for i in t])).replace('\n\r\n',''))
        # articles = articles[0].replace('\n\r\n','')
    if news_links == []:
        return 'На данный запрос не найдены новости. Введите новый запрос:'
    
    return articles, news_links