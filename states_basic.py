from aiogram.fsm.state import State , StatesGroup  , default_state 



class CheckSubscribe(StatesGroup):
    
    check = State()

class SendTZ(StatesGroup):
    send = State()


class SendMessage(StatesGroup):
    text = State()