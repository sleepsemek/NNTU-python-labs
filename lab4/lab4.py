import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import datetime

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

#Функция, которая парсит день недели с сайта
def parse_day_of_week(date_str):
    try:
        day, month, year = date_str.split('.')
        
        if not (1901 <= int(year) <= 2100):
            return "Введите дату 20 или 21 века"

        #Обращаемся к сайту калькулятору, подставляем в url введенную дату
        url = f"https://calendum.ru/Service/WeekdayByDate/{day}.{month}.{year}"
        #Заголовок взял из девтулз браузера
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 YaBrowser/26.4.0.0 Safari/537.36'}
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        #Ищем блок с результатом, молимся что верстка не изменится
        result_element = soup.find('span', class_='emstrong') 
        
        if result_element:
            return f"Дата: {date_str} \n День недели с сайта calendum.ru: {result_element.text.strip()}"
        else:
            return "День недели не найден, возможно на сайте изменилась верстка"
            
    except ValueError:
        return "Введите дату в формате ДД.ММ.ГГГГ."
    except:
        return "Произошла ошибка"

#Обработчики команд бота
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_calc = types.KeyboardButton('Узнать день недели')
    btn_help = types.KeyboardButton('Помощь')
    markup.add(btn_calc, btn_help)
    
    welcome_text = (f"Здравствуйте, {user_name}\n"
                    f"Я бот, который умеет определять день недели по любой дате 20 и 21 века.\n")
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)


@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "**Справка по боту**\n"
        "Этот бот парсит сайт calendum.ru, чтобы узнать, на какой день недели выпала определенная дата.\n"
        "- Поддерживаются даты с 1901 по 2100 год.\n"
        "- /start - перезапустить бота\n"
        "- /help - вызвать это меню"
    )
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Помощь':
        send_help(message)
    
    elif message.text == 'Узнать день недели':
        msg = bot.send_message(message.chat.id, "Напиши дату в формате ДД.ММ.ГГГГ", parse_mode='Markdown')
        #Следующее сообщение от пользователя отправляем в process_date_step
        bot.register_next_step_handler(msg, process_date_step)
        
    else:
        bot.send_message(message.chat.id, "Неизвестная команда, используй кнопки меню ниже или /help")


def process_date_step(message):
    date_str = message.text.strip()
    
    if date_str == 'Помощь' or date_str == '/help':
        send_help(message)
        return
    elif date_str == '/start':
        send_welcome(message)
        return

    #Сообщение заглушка на время загрузки
    wait_msg = bot.send_message(message.chat.id, "Пинаем сайт...")
    
    result = parse_day_of_week(date_str)
    
    #Редактируем заглушку на возвращенный результат
    bot.edit_message_text(chat_id=message.chat.id, message_id=wait_msg.message_id, text=result)


if __name__ == '__main__':
    print("Бот запущен")
    bot.polling(none_stop=True)
