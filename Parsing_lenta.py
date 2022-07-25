import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import re

def lenta_parse(req, max_num):
    request_txt = req

    link = f'https://lenta.ru/search?query={request_txt}#size=10|sort=2|domain=1|modified,format=yyyy-MM-dd'

    def clean_and_lemmatize(text):
        #cleaning
        text = re.sub(r'(\<(/?[^>]+)>)', '', text)
        return text
    
    def get_search_page(link):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        chrome_options = webdriver.ChromeOptions()
#         chrome_options.binary_location = "/usr/share/man/man1/google-chrome.1.gz"
        chrome_driver_binary = "./chromedriver"
       # driver = webdriver.Chrome(executable_path='/home/elena/workspace/ds_bootcamp/learning/Project/final_project/chromedriver_linux64/chromedriver', service_log_path='/home/alex/Desktop/final_project/chromedriver_linux64/chromedriver/geckodriver.log', options=options)
            
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver = webdriver.Chrome()
        driver.get(link)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source)
        return soup

    start = time.time()
    s = get_search_page(link)
    print(f'get_search_page working time: {time.time()-start}')
    lent_links=[]
    start = time.time()
    for i in s.find_all('div', attrs = {'class' : 'b-search__result-item-title'}):
        lent_links.append(i.a.attrs['href'])
    print(f'find_all working time: {time.time()-start}')
    f = []

    
    for i in range(max_num):#range(len(lent_links)):    
        song_url = lent_links[i]
        song_page = requests.get(song_url)
        song_html = BeautifulSoup(song_page.text, 'html.parser')
        t = song_html.find_all('p', attrs = {'class' : 'topic-body__content-text'})
        # print(clean_and_lemmatize(''.join([str(i) for i in t])))
        f.append(clean_and_lemmatize(''.join([str(i) for i in t])))
    return f, lent_links[:max_num]




