from telebot import TeleBot, types
from faker import Faker


bot = TeleBot(token='TOKEN', parse_mode='html') # создание бота

faker = Faker("ru_RU") # утилита для генерации фейковых тестовых данных

# объект клавиаутры
card_type_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

# Кнопки 
card_type_keyboard.row(
    types.KeyboardButton(text='VISA'),
    types.KeyboardButton(text='Mastercard'),
    types.KeyboardButton(text='Maestro'),
    types.KeyboardButton(text='test'),
)

# обработчик команды '/start'
@bot.message_handler(commands=['start'])
def start_command_handler(message: types.Message):
    # отправляем ответ на команду '/start'
    bot.send_message(
        chat_id=message.chat.id, # id чата, в который необходимо направить сообщение
        text='Привет! Я умею генерировать данные тестовой банковской карты VISA, Mastercard и Maestro \nВыбери тип карты:', # текст сообщения
        reply_markup=card_type_keyboard,
    )

# обработчик всех остальных сообщений
@bot.message_handler()
def message_handler(message: types.Message):
    # проверяем текст сообщения на совпадение с текстом какой либо из кнопок
    # в зависимости от типа карты присваиваем значение переменной 'card_type'
    if message.text == 'VISA':
        card_type = 'visa'
    elif message.text == 'Mastercard':
        card_type = 'mastercard'
    elif message.text == 'Maestro':
        card_type = 'maestro'
    else:
        # если текст не совпал ни с одной из кнопок 
        # выводим ошибку
        bot.send_message(
            chat_id=message.chat.id,
            text='Не понимаю тебя :(',
        )
        return

    # получаем данные тестовой карты выбранного типа
    # card_type может принимать одно из зачений ['maestro', 'mastercard', 'visa13', 'visa16', 'visa19',
    # 'amex', 'discover', 'diners', 'jcb15', 'jcb16']
    card_information = faker.credit_card_full(card_type)           
    # и выводим пользователю
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Данные тестовой карты:\n<code>{card_information}</code>'
    )

# главная функция программы
def main():
    # запускаем нашего бота
    bot.infinity_polling()


if __name__ == '__main__':
    main()
