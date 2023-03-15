import requests
import random
import urllib.parse
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

logging.basicConfig(filename="main.log", level=logging.DEBUG, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")
load_dotenv()
newsApi_url = os.environ.get('newsApi_url')


def get_title_of_random_news():
    # Getting news by api
    params = {
      "apiKey": os.environ.get('newsApi_key'),
      "q": "велосипед OR велосипедист OR вело OR велопрогулка OR велокража OR Велопутешествие OR Велопадение OR Велотравма"
            " OR велодорожка OR MTB OR велопарковка OR велопоездка OR BMX OR электровелосипед OR велоавария OR"
           " программирование OR программист OR компьютер OR компьютерный OR Персональный компьютер OR программирования"
           " OR python OR java OR C# OR assembler OR IT OR информационные технологии ",
      # "q": "-война AND -спецоперация AND -СВО AND -Киев AND -Москва AND -Киевский AND -Украина AND -Украинский AND -Украинские AND -Украинских AND -оружие AND -оружия AND -обстрел AND -обстрелы AND -удар AND -удары AND -ракетный AND -Украине AND -Украины AND -ракетных",
      "searchIn": "title",
      "sources": "",
      "domains": "",
      "excludeDomains": "pikabu.ru",
      "from": "",
      "to": "",
      "language": "ru",
      "sortBy": "popularity",
      "pageSize": "100",
      "page": "1"
    }

    res = requests.get(url=newsApi_url+'everything', params=urllib.parse.urlencode(params))
    # Counting news in response and choosing random news
    countOfNews = len(res.json().get('articles'))
    numberNews = random.randint(0, countOfNews-1)
    # Ejecting url and title of random news
    urlNews = res.json().get('articles')[numberNews]['url']
    titleNewsRu = res.json().get('articles')[numberNews]['title']
    print(urlNews, titleNewsRu)
    log.info(f"ARTICLES: {res.json().get('articles')}\n\n titleNewsRu: {titleNewsRu}\n urlNews:{urlNews}")
    return titleNewsRu


def get_list_of_news():
    # Getting news by api
    params = {
      "country": "ru",
      "q": "",
      "apiKey": os.environ.get('newsApi_key'),
      "sources": "",
      "pageSize": "100",
      "page": "1"
    }

    res = requests.get(url=newsApi_url+'top-headlines', params=urllib.parse.urlencode(params))
    # Ejecting url and title of random news
    news_list = res.json().get('articles')
    log.info(f"{res.json().get('articles').__len__()} articles has been found:\n\n{res.json().get('articles')}\n\n")
    return news_list
