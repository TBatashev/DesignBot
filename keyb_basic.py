from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton



def get_tz(user_id):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Получить ТЗ', callback_data=f'get_tz_{user_id}'))

    return kb.as_markup()


def send_channel(user_id=0):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Подписаться на канал', url='https://t.me/+wVTllgIhHrM2ZTRi'))
    # kb.add(InlineKeyboardButton(text='Проверить подписку', callback_data=f'check_{user_id}'))

    return kb.as_markup()

def send_tz(user_id):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Отправить работу', callback_data=f'sendtz_{user_id}'))

    return kb.as_markup()


def get_adm():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Информация о боте', callback_data=f'all_users'))

    kb.add(InlineKeyboardButton(text='Рассылка среди юзеров', callback_data='rassil_users'))



    return kb.as_markup()