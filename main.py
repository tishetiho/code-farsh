import asyncio, logging
from datetime import datetime
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandObject
from aiogram.types import LabeledPrice, PreCheckoutQuery

from config import API_TOKEN, ADMIN_ID, USD_RATE
from database import Database
from logic import AIService, PaymentService, Games
import keyboards as kb

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- [ СТАРТ И РЕГИСТРАЦИЯ ] ---
@dp.message(Command("start"))
async def start(m: types.Message, command: CommandObject):
    ref = int(command.args) if command.args and command.args.isdigit() else 0
    await Database.conn.execute("INSERT OR IGNORE INTO users (id, ref_l1, joined) VALUES (?, ?, ?)",
                                (m.from_user.id, ref, datetime.now().isoformat()))
    await Database.conn.commit()
    await m.answer("🪐 EMPIRE OS v43.0 запущен. Выберите сектор:", 
                   reply_markup=kb.main_kb(m.from_user.id, ADMIN_ID))

# --- [ АВТО-ШОП ] ---
@dp.callback_query(F.data == "shop_main")
async def shop_menu(c: types.CallbackQuery):
    cursor = await Database.conn.execute("SELECT DISTINCT category FROM shop_items WHERE stock > 0")
    cats = [r[0] for r in await cursor.fetchall()]
    await c.message.edit_text("🛒 КАТЕГОРИИ МАРКЕТА", reply_markup=kb.shop_cat_kb(cats))

@dp.callback_query(F.data.startswith("cat_"))
async def show_items(c: types.CallbackQuery):
    cat = c.data.split("_")[1]
    items = await (await Database.conn.execute("SELECT * FROM shop_items WHERE category = ?", (cat,))).fetchall()
    text = f"📦 ТОВАРЫ В {cat}:\n\n"
    kb_builder = InlineKeyboardBuilder()
    for i in items:
        text += f"🔹 {i['name']} — {i['price']}₽\n"
        kb_builder.add(types.InlineKeyboardButton(text=f"Купить {i['name']}", callback_data=f"buy_item_{i['id']}"))
    await c.message.edit_text(text, reply_markup=kb_builder.as_markup())

@dp.callback_query(F.data.startswith("buy_item_"))
async def buy_item(c: types.CallbackQuery):
    i_id = c.data.split("_")[2]
    user = await Database.get_user(c.from_user.id)
    item = await (await Database.conn.execute("SELECT * FROM shop_items WHERE id = ?", (i_id,))).fetchone()
    
    if user['bal'] >= item['price']:
        await Database.conn.execute("UPDATE users SET bal = bal - ? WHERE id = ?", (item['price'], c.from_user.id))
        await Database.conn.execute("UPDATE shop_items SET stock = stock - 1 WHERE id = ?", (i_id,))
        await Database.conn.commit()
        await c.message.answer(f"✅ ПОКУПКА ЗАВЕРШЕНА!\n\nВаш товар:\n{item['data']}")
    else:
        await c.answer("❌ Недостаточно средств!", show_alert=True)

# --- [ ПОПОЛНЕНИЕ: STARS & CRYPTO ] ---
@dp.callback_query(F.data == "deposit")
async def dep_choice(c: types.CallbackQuery):
    await c.message.answer_invoice(
        title="100 Кредитов Империи", description="Пополнение баланса XTR",
        payload="dep_100", currency="XTR", prices=[LabeledPrice(label="XTR", amount=50)]
    )

@dp.pre_checkout_query()
async def pre_checkout(pq: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pq.id, ok=True)

@dp.message(F.successful_payment)
async def pay_ok(m: types.Message):
    await Database.conn.execute("UPDATE users SET bal = bal + 100 WHERE id = ?", (m.from_user.id,))
    await Database.conn.commit()
    await m.answer("🌟 Баланс успешно пополнен через Stars!")

# --- [ ЗАПУСК ] ---
async def runner():
    await Database.init()
    logging.basicConfig(level=logging.INFO)
    print("🚀 EMPIRE OS v43.0: ONLINE")
    await dp.start_polling(bot)

if __name__ == "main":
    asyncio.run(runner())
