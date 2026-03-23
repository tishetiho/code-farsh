from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def main_kb(uid, admin_id):
    kb = InlineKeyboardBuilder()
    kb.row(types.InlineKeyboardButton(text="🛒 ШОП", callback_data="shop_main"),
           types.InlineKeyboardButton(text="🤝 P2P БИРЖА", callback_data="p2p_main"))
    kb.row(types.InlineKeyboardButton(text="🎰 КАЗИНО", callback_data="casino"),
           types.InlineKeyboardButton(text="📩 ПОЧТА", callback_data="mail"))
    kb.row(types.InlineKeyboardButton(text="👤 ПРОФИЛЬ", callback_data="me"),
           types.InlineKeyboardButton(text="💰 ПОПОЛНИТЬ", callback_data="deposit"))
    if uid == admin_id:
        kb.row(types.InlineKeyboardButton(text="⚙️ АДМИНКА", callback_data="admin"))
    return kb.as_markup()

def shop_cat_kb(cats):
    kb = InlineKeyboardBuilder()
    for cat in cats:
        kb.add(types.InlineKeyboardButton(text=cat, callback_data=f"cat_{cat}"))
    kb.adjust(2)
    return kb.as_markup()

def games_kb():
    kb = InlineKeyboardBuilder()
    kb.row(types.InlineKeyboardButton(text="🎰 КРУТИТЬ (50₽)", callback_data="play_slots"))
    kb.row(types.InlineKeyboardButton(text="⬅️ НАЗАД", callback_data="me"))
    return kb.as_markup()
    
