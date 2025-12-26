import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

TOKEN = "8222141186:AAHFzeflGO2oO5pQ-RnwSXWG7apsfak-AKU"
ADMIN_ID = 7426345695  # O'Z TELEGRAM ID
CHANNEL = "@movemegroup"

bot = Bot(token=TOKEN)
dp = Dispatcher()


class Form(StatesGroup):
    name = State()
    phone = State()
    level = State()


@dp.message(Command("start"))
async def start(message: types.Message):
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="🔔 Kanalga obuna bo‘lish", url=f"https://t.me/{CHANNEL.replace('@','')}")],
            [types.InlineKeyboardButton(text="✅ Tekshirish", callback_data="check")]
        ]
    )
    await message.answer(
        "👋 Botdan foydalanish uchun kanalga obuna bo‘ling:",
        reply_markup=kb
    )


@dp.callback_query(lambda c: c.data == "check")
async def check_sub(call: types.CallbackQuery, state: FSMContext):
    try:
        member = await bot.get_chat_member(CHANNEL, call.from_user.id)
        if member.status in ["member", "administrator", "creator"]:
            await call.message.answer("✍️ Ismingizni kiriting:")
            await state.set_state(Form.name)
        else:
            await call.answer("❌ Avval kanalga obuna bo‘ling!", show_alert=True)
    except:
        await call.answer("❌ Kanal topilmadi yoki obuna yo‘q", show_alert=True)


@dp.message(Form.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)

    kb = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]],
        resize_keyboard=True
    )
    await message.answer("📞 Telefon raqamingizni yuboring:", reply_markup=kb)
    await state.set_state(Form.phone)


@dp.message(Form.phone)
async def get_phone(message: types.Message, state: FSMContext):
    if not message.contact:
        await message.answer("❗ Iltimos, tugma orqali telefon yuboring")
        return

    await state.update_data(phone=message.contact.phone_number)

    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Intermediate")],
            [types.KeyboardButton(text="Advanced")]
        ],
        resize_keyboard=True
    )

    await message.answer("🇬🇧 Ingliz tili darajangizni tanlang:", reply_markup=kb)
    await state.set_state(Form.level)


@dp.message(Form.level)
async def finish(message: types.Message, state: FSMContext):
    data = await state.get_data()

    await bot.send_message(
        ADMIN_ID,
        f"🆕 YANGI MIJOZ\n\n"
        f"👤 Ism: {data['name']}\n"
        f"📞 Telefon: {data['phone']}\n"
        f"📘 Daraja: {message.text}"
    )

    await message.answer(
        "✅ Rahmat! Siz bilan tez orada bog‘lanamiz.\n"
        "📌 Batafsil ma’lumot: https://t.me/com3n",
        reply_markup=types.ReplyKeyboardRemove()
    )

    await state.clear()


async def main():
    print("✅ Bot ishga tushdi")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
