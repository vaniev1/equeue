import telebot
import requests
from bs4 import BeautifulSoup


bot = telebot.TeleBot('token')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Введите номер своего автомобиля:')

def search_on_website(search_query):
    url = 'https://codd15.ru/include/seek.php'
    data = {'search': search_query}
    response = requests.post(url, data=data)
    soup = BeautifulSoup(response.content, 'html.parser')
    position_div = soup.find('div', class_='text-center')
    position_text = position_div.text.strip()
    position_parts = [part.strip() for part in position_text.split('\n') if part.strip()]
    position = position_parts[-5] + '\n' + position_parts[-4] + '\n' + position_parts[-3] + '\n' + position_parts[-2] + '\n' + position_parts[-1]
    position = position.replace('<br>', ' ').replace('  ', ' ')
    return position



@bot.message_handler(content_types=['text'])
def send_text(message):
    car_number = message.text
    # выполнение запроса на сайт и получение информации о позиции автомобиля в очереди
    position_in_queue = search_on_website(car_number)
    bot.send_message(message.chat.id, f'Ваш автомобиль {position_in_queue}')


bot.polling()