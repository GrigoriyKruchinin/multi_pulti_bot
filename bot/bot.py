import asyncio
import logging

from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from config import INLINE_KEYBOARD, KEYBOARD, TOKEN, ChoiceCallback, Form


bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Добро пожаловать в наш бот!", reply_markup=KEYBOARD)


@router.message(Command("help"))
async def help(message: types.Message):
    await message.answer(
        "Доступные команды: /start, /help, /echo, /photo, /inline, /start_fsm"
    )


@router.message(Command("echo"))
async def echo(message: types.Message):
    if len(message.text) > len("/echo "):
        await message.answer(message.text[len("/echo ") :])
    else:
        await message.answer("Пожалуйста, введите текст после команды /echo.")


@router.message(Command("inline"))
async def inline(message: types.Message):
    await message.answer("Сделайте выбор:", reply_markup=INLINE_KEYBOARD)


@router.callback_query(ChoiceCallback.filter())
async def choice_callback(
    callback_query: types.CallbackQuery, callback_data: ChoiceCallback
):
    option = callback_data.option
    if option == "1":
        await callback_query.message.answer("Вы выбрали Выбор 1")
    elif option == "2":
        await callback_query.message.answer("Вы выбрали Выбор 2")
    await callback_query.answer()


@router.message(Command("start_fsm"))
async def start_fsm(message: types.Message, state: FSMContext):
    await message.answer("Как вас зовут?")
    await state.set_state(Form.name)


@router.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько вам лет?")
    await state.set_state(Form.age)


@router.message(Form.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    user_data = await state.get_data()
    await message.answer(
        f"Ваше имя: {user_data['name']}, ваш возраст: {user_data['age']}"
    )
    await state.clear()


@router.message(Command("photo"))
async def inline(message: types.Message):
    await message.answer("Пришлите фото, а мы пришлем вам его размеры!")


@router.message(F.photo)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    await message.answer(f"Размер изображения: {photo.width} x {photo.height} пикселей")


async def main():
    logging.basicConfig(level=logging.INFO)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
