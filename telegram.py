import telebot
import requests

bot_token = "5243412284:AAElbwcCDmKXOe4XTvG1F3EFdbDleAHH3ew"
bot = telebot.TeleBot(bot_token)
chat_id = "174958495"

def send_msg(text):
    url = "https://api.telegram.org/bot"+bot_token+"/sendMessage?chat_id="+chat_id+"parse_mode=Markdown&text="
    req = url+text
    response = requests.get(req)
    return response.json()


def send_photo(path):
    img = open(path, 'rb')

    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto?chat_id={chat_id}'

    respon = requests.post(url, files={'photo': img})
    return respon.json()


