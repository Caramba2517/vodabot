from aiogram.dispatcher.filters.state import StatesGroup, State

class Register(StatesGroup):
    info = State()

class Sinop(StatesGroup):
    el = State()
    hvs = State()
    gvs = State()

class Fasol(StatesGroup):
    el_d = State()
    el_n = State()

class RC(StatesGroup):
    el = State()

class Admin(StatesGroup):
    user_id = State()
    info = State()