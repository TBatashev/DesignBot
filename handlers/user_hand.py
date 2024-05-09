from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message, ChatJoinRequest
from aiogram.fsm.context import FSMContext
from aiogram.filters import  StateFilter

from states_basic import CheckSubscribe, SendTZ
from keyb_basic import get_tz, send_channel, send_tz
from database.database import DB
import time
from datetime import datetime


router = Router()


@router.message(F.text == '/start')
async def start_user(msg : Message, bot : Bot, state : FSMContext):

    user_channel_status = await bot.get_chat_member(chat_id='-1001965820833', user_id=msg.from_user.id)
    if user_channel_status.status != 'left':
        with DB() as db :
            db.save_user(int(msg.from_user.id))
            db.username_start(msg.from_user.username,  int(msg.from_user.id))
            today = datetime.now().date()
            db.save_date(user=int(msg.from_user.id), date=today)
        await msg.answer(text='Добро пожаловать, чтобы получить тз нажмите кнопку ниже', reply_markup=get_tz(msg.from_user.id))

    else:
        await bot.send_message(msg.from_user.id, 'Вы не подписались на канал, пожалуйста подпишитесь', reply_markup=send_channel())
        await state.set_state(CheckSubscribe.check)



@router.message(F.text == 'cancel', ~StateFilter(None))
async def cancel(msg : Message, state : FSMContext):
    await state.clear()




@router.chat_join_request()
async def join_to_group(update : ChatJoinRequest, bot : Bot):
    user_id = update.from_user.id
    update.answer(message_thread_id=user_id ,text='')

    try :
        # await bot.delete_message(chat_id=user_id)
        await bot.send_message(chat_id=user_id, text='Нажмите /start для продолжения.')
        await update.approve()

    except :
        print('Ошибка отправки сообщения заявленному юзеру')

last_command_time = 0
command_count = 0



@router.callback_query(F.data.startswith('get_tz'))
async def gett_tz(call : CallbackQuery):
    try :
        global last_command_time, command_count

        await call.answer()
        current_time = time.time()
        if command_count == 2:
            if current_time - last_command_time > 600:
                command_count = 0
            else :
                await call.message.answer('Похоже вы потратили лимит. Подождите до 10минут')
        last_command_time = current_time
    
        if command_count < 2:
            command_count += 1
            with DB() as db:
                rand = db.get_random_tz()
            userid = call.from_user.id
            await call.message.answer(text=rand, reply_markup=send_tz(userid))

    except Exception as e:
        print(e)


@router.callback_query(F.data.startswith('sendtz'))
async def send_t_z(call : CallbackQuery, state : FSMContext):
    try :

        userid = call.data.split('_')[1]
        await call.answer('Отправьте работу в формате изображения или документа')
        await call.answer()

        await state.set_state(SendTZ.send)
    
    except :
        pass

@router.message(StateFilter(SendTZ.send))
async def get_work_user(msg : Message, state : FSMContext, bot : Bot):
    try :
        if msg.document :
            doc = msg.document.file_id
            doc_id = msg.message_id
            await bot.send_document(chat_id='-1001965820833', document=doc, caption=f'Ид: {msg.from_user.id} | Юзернейм: @{msg.from_user.username}')
            await msg.answer('Работа успешно отправлена')

            await state.clear()
        
        elif msg.photo :
            photo_id = msg.message_id
            photo = msg.photo[-1].file_id
            await bot.send_photo(chat_id='-1001965820833', photo=photo, caption=f'Ид: {msg.from_user.id} | Юзернейм: @{msg.from_user.username}')
            await msg.answer('Работа успешно отправлена')
            await state.clear()
        
        else :
            await msg.answer('Вы отправили что-то не то. Попробуйте еще раз')
            global command_count
            command_count -= 1
            await state.clear()

    
    except :
        pass



