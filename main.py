import os
import logging
from dotenv import load_dotenv
import openai
from aiogram import Bot, Dispatcher, executor, types
import aioschedule
import asyncio
import news
import ai
import random

import tools

# Configure logging
logging.basicConfig(filename="main.log", level=logging.DEBUG, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")

load_dotenv()
chat_id = os.environ.get('chat_id')
openai.api_key = os.environ.get('openai_api_key')
tgBot_url = os.environ.get('tgBot_url')
newsApi_url = os.environ.get('newsApi_url')
API_TOKEN = os.environ.get('tgBot_id')


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

sent_news_list = []

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Артемий Курицын - самое независимое СМИ в мире. Уникальный взгляд по всем вопросам.\n"
                        "Чтобы получить нейроновость - /neuroNews\n"
                        "Чтобы получить самую интересную настоящую новость - /topNews")


@dp.message_handler(commands=['neuroNews'])
async def add_members(message: types.Message):
    """
    This handler will be called when user sends `/news`
    """
    await message.reply(f"Спасибо за обращение. Вас запрос в очереди - {random.randrange(9999)}, ожидайте")
    titleNews = news.get_title_of_random_news()

    # Getting GPT opinion about news
    gpt_opinion = ai.get_opinion_about_news(titleNews)

    # making image for news
    image_url = ai.get_image_url_from_title(titleNews)

    # Sending message to telegram bot
    await message.answer_photo(photo=image_url, parse_mode="HTML", caption=f"<b>{titleNews}</b>{gpt_opinion}")


@dp.message_handler(commands=['topNews'])
async def add_members(message: types.Message):
    """
    This handler will be called when user sends `/news`
    """
    await message.reply(f"Спасибо за обращение. Вас запрос в очереди - {random.randrange(9999)}, ожидайте")

    # Ask newsapi about top news
    news_list = news.get_list_of_news()

    # Making a string with titles
    titles_string = ""
    for i in news_list:
        if not tools.is_string_exist_in_list(i['title'], sent_news_list):
            titles_string = titles_string + '"' + i['title'] + '",'
            if titles_string.__len__() > 3000:
                break

    # Ask GPT to choose the most funny news
    top_news_title = ai.choose_the_best_news(titles_string)
    sent_news_list.append(top_news_title)
    print(sent_news_list)
    # find url of top news
    top_news_url = ""
    for i in news_list:
        if tools.is_string_equal(top_news_title, i['title']):
            top_news_url = i['url']

    # making image for news
    image_url = ai.get_image_url_from_title(top_news_title)

    # Sending message to telegram bot
    await message.answer_photo(photo=image_url, parse_mode="HTML", caption=f'<b>{top_news_title}</b>\n'
                                                                           f'<a href="{top_news_url}">подробнее</a>')

@dp.message_handler(commands=['helloBot'])
async def add_members(message: types.Message):
    await message.answer(text="/m2m Привет, бот!")


async def send_wishes():
    pass


async def scheduler():
    aioschedule.every(20).seconds.do(send_wishes)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)