from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder



def main_kb(username):
    kb_list = [
        [KeyboardButton(text="⬆ Пополнить"), KeyboardButton(text="⬇ Вывести")],
        [KeyboardButton(text="📃 Инструкция"), KeyboardButton(text="👤 Профиль")]
        
    ]
    if username == "jbn9991" or username == "zetadmin" or username == "@jbb8891" or username == "@zetadmin":
     kb_list.append([KeyboardButton(text="⚙️ Настройки")])
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Что вы хотите сделать:")
    return keyboard

def main_cancel_kb():
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отменить")]], resize_keyboard=True, one_time_keyboard=True)
    return keyboard

def main_id_kb(xid):
    kb_list = [
        [KeyboardButton(text=str(xid))],
        [KeyboardButton(text="Отменить")]
    ]
    
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

def main_admin_kb():
    kb_list = [
        [KeyboardButton(text="Редактировать службу поддержки")],
        [KeyboardButton(text="Редактировать реквизиты")],
        [KeyboardButton(text="Загрузить другой QR")],
        [KeyboardButton(text="Добавить реквизит")],
        [KeyboardButton(text="Отменить")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Что вы хотите сделать?")
    return keyboard


def main_admin_props_kb(main_props, props):
    kb_list = [[KeyboardButton(text=main_props + " ⭐")]]
    
    for prop in props:
        kb_list.append([KeyboardButton(text=prop)])
    kb_list.append([KeyboardButton(text="Отменить")])
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

def main_admin_props_edit_kb():
    kb_list = [
        [KeyboardButton(text="Удалить")],
        [KeyboardButton(text="Отменить")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard
    



def main_inline_replenish_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="По номеру телефона (Любой банк)", callback_data="replenish1")
    )
    builder.row(
        InlineKeyboardButton(text="Через QR (Любой банк)", callback_data="replenish2")  
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=builder.export())
    return keyboard

def main_inline_withdraw_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="МБАНК", callback_data="withdraw1"),
        InlineKeyboardButton(text="О Деньги!", callback_data="withdraw2")
    )
    builder.row(
        InlineKeyboardButton(text="По номеру карты", callback_data="withdraw3")
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=builder.export())
    return keyboard


def main_inline_admin_replenish_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Одобрить", callback_data="accept"),
        InlineKeyboardButton(text="Отклонить", callback_data="cancel"),
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=builder.export())
    return keyboard

def main_inline_admin_withdraw_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Одобрить", callback_data="waccept"),
        InlineKeyboardButton(text="Отклонить", callback_data="wcancel"),
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=builder.export())
    return keyboard


def subscribe_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Подписаться", url="https://t.me/zetkassakg"),
        InlineKeyboardButton(text="Проверить", callback_data="subscribe"),
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=builder.export())
    return keyboard

def payment_kb(url):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Оплатить", url=url or "https://t.me/zetkassakg"),
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=builder.export())
    return keyboard

def block_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Заблокировать", callback_data="block_user"),
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=builder.export())
    return keyboard

def unblock_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Разблокировать", callback_data="unblock_user"),
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=builder.export())
    return keyboard