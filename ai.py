import os
import logging
from dotenv import load_dotenv
import openai


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


# def get_opinion_about_news(title):
#     # Getting GPT opinion about news
#     log.info(f"Send request to make neuro news.\nTitle: {title}\n\n")
#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=f"Ты - ведущий новостей. Придумай смешную нелепую новость с этим заголовком {title}. Опиши время и место. Придумай шутку. Можешь писать грубо",
#         # prompt=f"You are a newsmaker. Make a ridiculous funny news about this {title}. Decribe place. make a joke. Be rude if you want",
#         # prompt=f"{titleNewsEnText} What do you think? Say word \"crap\" or \"awesome\" then your opinion. Be be extremely positive and sweet",
#         # prompt=f"Create funny ridiculous news about bicycle. Describe date and place. Create title. ",
#         # prompt=f"Make a ridiculous funny news about this The most nord northern in the world. Decribe place and date. make a joke. Be rude if you want",
#         temperature=0.7,
#         max_tokens=1000,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )
#     print(response['choices'][0]['text'])
#     log.info(f"Neuro news title: {response['choices'][0]['text']}\n\n")
#     return response['choices'][0]['text']


# def choose_the_best_news(titles_string):
#     log.info(f"Send request to choose the best news.\nTitles: {titles_string}\n\n")
#     # make GPT choose tho most funny news
#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=f"Выбери самую забавную и смешную новость из списка: {titles_string}",
#         temperature=0.7,
#         max_tokens=1000,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )
#     print(response['choices'][0]['text'])
#     log.info(f"Chosen news title: {response['choices'][0]['text']}\n\n")
#     return response['choices'][0]['text']


# def get_argument_about_news(title):
#     log.info(f"Send request to choose the best news.\nTitles: {title}\n\n")
#     # make GPT choose tho most funny news
#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=f"Объясни, почему эта новость забавная и приятная: {title}",
#         temperature=0.7,
#         max_tokens=1000,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )
#     print(response['choices'][0]['text'])
#     log.info(f"Chosen news title: {response['choices'][0]['text']}\n\n")
#     return response['choices'][0]['text']


def ask_chatGPT(model="text-davinci-003", prompt="Привет", temperature=0.7, max_tokens=1000, top_p=1,
                frequency_penalty=0, presence_penalty=0):
    log.info(f"Asking GPT with:\n{prompt}")
    # make GPT choose tho most funny news
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )
    print(response['choices'][0]['text'])
    log.info(f"GPT's responce: {response['choices'][0]['text']}\n\n")
    return response['choices'][0]['text']





def get_image_url_from_title(title):
    # making image for news
    log.info(f"Send request to make an image from title:: {title}\n\n")
    try:
        response = openai.Image.create(
            prompt=title,
            n=1,
            size="512x512"
        )
        log.info(f"Success, url of image: {response['data'][0]['url']}\n\n")
        return response['data'][0]['url']
    except Exception as e:
        log.info(f"ERROR {e}\n\n")
        return None

