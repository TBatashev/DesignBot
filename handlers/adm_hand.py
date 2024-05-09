import asyncio
from aiogram import Router , F , Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import BaseFilter , StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from configs import conf_admins
from keyb_basic import get_adm
from database.database import DB
from states_basic import SendMessage

class IsAdmin(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in conf_admins

router = Router()
router.message.filter(IsAdmin())



@router.message(F.text == '/admin')
async def start_admin(msg : Message):
    await msg.answer('Вы вошли в админ-панель', reply_markup=get_adm())


@router.callback_query(F.data == 'all_users')
async def get_users_all(call : CallbackQuery):
    try :
        with DB() as db:
            all_users = db.get_all_users(count=1)
            day_users = db.get_count_users_last_day()
            week_users = db.get_count_users_last_week()
            month_users = db.get_count_users_last_month()
        
        await call.message.edit_text(text=f'''Все пользователи : {all_users}
За последний день : {day_users}\nЗа неделю : {week_users}\nЗа месяц : {month_users}''', reply_markup=get_adm())

    
    except Exception as e :
        print(e)


@router.callback_query(F.data == 'rassil_users')
async def send_rassil(call : CallbackQuery, bot : Bot, state : FSMContext):
    try:
        await call.message.answer('Введите текст для рассылки ( возможно так же прикрепить фотографию)')
        await state.set_state(SendMessage.text)
        # with DB() as db:
        #     users = db.get_all_users(rassil=1)
        #     for user in users :

    except :
        pass


@router.message(StateFilter(SendMessage.text))
async def message_send(msg : Message, state : FSMContext, bot : Bot):
    if msg.photo:
        photo = msg.photo[-1].file_id
        text = msg.caption
        # await msg.answer_photo(photo=photo, caption=text)
    else :
        text = msg.text
        # await msg.answer(f"{text}")

    with DB() as db :
        users = db.get_all_users(rassil=1)
        
        for user in users :
            try :
                if msg.photo:
                    await bot.send_photo(chat_id=user[1], photo=photo, caption=text)
                    print('Сообщение отправилось')
                    await asyncio.sleep(1)
                else :
                    await bot.send_message(chat_id=user[1], text=text)
                    print('Сообщение отправилось')
                    await asyncio.sleep(1)

            except Exception as ex:
                print(f'Сообщение не отправилось. Ошибка {ex}')
                continue

    

    await state.clear()


@router.message(F.text.startswith('/add'))
async def add_tz(msg : Message):
    try :
        tz = msg.text.split(' ')[2:]
        tz2 = ' '.join(tz)
        with DB() as db :
            db.add_tz(tz2)
    
    except :
        pass