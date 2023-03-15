import os
from operator import itemgetter
import datetime
import time
import logging
import sys
import base64
from dotenv import load_dotenv
import pytz
import requests
import openai
import random
from googletrans import Translator
import urllib.parse
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile
import aioschedule
import asyncio
import time
import re
import random


# Configure logging
logging.basicConfig(filename="main.log", level=logging.DEBUG, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")

load_dotenv()
chat_id = os.environ.get('chat_id')
openai.api_key = os.environ.get('openai.api_key')
tgBot_url = os.environ.get('tgBot_url')
newsApi_url = os.environ.get('newsApi_url')
API_TOKEN = os.environ.get('tgBot_id')


def get_opinion_about_news(title):
    # Getting GPT opinion about news
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Ты - ведущий новостей. Придумай смешную нелепую новость с этим заголовком {title}. Опиши время и место. Придумай шутку. Можешь писать грубо",
        # prompt=f"You are a newsmaker. Make a ridiculous funny news about this {title}. Decribe place. make a joke. Be rude if you want",
        # prompt=f"{titleNewsEnText} What do you think? Say word \"crap\" or \"awesome\" then your opinion. Be be extremely positive and sweet",
        # prompt=f"Create funny ridiculous news about bicycle. Describe date and place. Create title. ",
        # prompt=f"Make a ridiculous funny news about this The most nord northern in the world. Decribe place and date. make a joke. Be rude if you want",
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response['choices'][0]['text'])
    return response['choices'][0]['text']


def choose_the_best_news(titles_string):

    # make GPT choose tho most funny news
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Выбери самую забавную новость из списка: {titles_string}",
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response['choices'][0]['text'])
    return response['choices'][0]['text']


def get_image_url_from_title(title):
    # making image for news
    response = openai.Image.create(
        prompt=title,
        n=1,
        size="512x512"
    )
    return response['data'][0]['url']