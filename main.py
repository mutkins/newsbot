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
async def neuro_news(message: types.Message):
    """
    This handler will be called when user sends `/news`
    """
    log.debug("neuroNews handler\n\n")
    await message.reply(f"Спасибо за обращение. Вас запрос в очереди - {random.randrange(9999)}, ожидайте")
    titleNews = news.get_title_of_random_news()

    # Getting GPT opinion about news
    gpt_opinion = ai.ask_chatGPT(
        prompt=f"Ты - ведущий новостей. Придумай смешную нелепую новость с этим заголовком {titleNews}."
               f" Опиши время и место. Придумай шутку. Можешь писать грубо")

    # making image for news
    image_url = ai.get_image_url_from_title(titleNews)

    # Sending message to telegram bot
    await message.answer_photo(photo=image_url, parse_mode="HTML", caption=f"<b>{titleNews}</b>{gpt_opinion}")


@dp.message_handler(commands=['topNews'])
async def top_news(message: types.Message):
    """
    This handler will be called when user sends `/news`
    """
    log.debug("topNews handler\n\n")
    await message.reply(f"Спасибо за обращение. Вас запрос в очереди - {random.randrange(9999)}, ожидайте")

    # Ask newsapi about top news
    news_list = news.get_list_of_news()

    # Making a string with titles
    titles_string = ""
    for item in news_list:
        if not tools.is_string_exist_in_list(item['title'], sent_news_list):
            titles_string = titles_string + '"' + item['title'] + '",'
            if titles_string.__len__() > 3000:
                break

    # Ask GPT to choose the most funny news
    top_news_title = ai.ask_chatGPT(prompt=f"Выбери самую забавную и смешную новость из списка: {titles_string}")

    sent_news_list.append(top_news_title)
    print(sent_news_list)

    # find url of top news
    top_news_url = ""
    for item in news_list:
        if tools.is_string_equal(top_news_title, item['title']):
            top_news_url = item['url']
            break

    log.debug(f"Top news title = {top_news_title}, Top news url = {top_news_url}\n\n")
    # Get original url of news (not googlenews)
    log.debug(f"Converting topnewsurl to original")
    top_news_url = tools.get_original_url_of_news(top_news_url)
    log.debug(f"Top news title = {top_news_title}, Top news url = {top_news_url}\n\n")

    # making image for news
    # image_url = ai.get_image_url_from_title(top_news_title)

    # Sending message to telegram bot
    # if image_url:
    #     await message.answer_photo(photo=image_url, parse_mode="HTML", caption=f'<b>{top_news_title}</b>\n'
    #                                                                        f'<a href="{top_news_url}">подробнее</a>')
    # else:
    await message.answer(text=f'<b>{top_news_title}</b>\n<a href="{top_news_url}">подробнее</a>',parse_mode="HTML")


@dp.message_handler(commands=['what'])
async def argument(message: types.Message):
    """
    This handler will be called when user sends `/news`
    """
    log.debug("argument handler\n\n")
    await message.reply(f"Спасибо за обращение. Вас запрос в очереди - {random.randrange(9999)}, ожидайте")
    gpt_argument = ai.ask_chatGPT(prompt=f"{message.reply_to_message.text} {message.get_args()}?")
    # Sending message to telegram bot
    await message.reply(text=gpt_argument)


async def send_wishes():
    pass


async def scheduler():
    aioschedule.every(60).seconds.do(send_wishes)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)