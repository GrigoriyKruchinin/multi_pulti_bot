from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.context import FSMContext

from states import Form, LastMsg
from config import INLINE_KEYBOARD, KEYBOARD, ChoiceCallback
from middlewares import SlowpokeMiddleware

router = Router()
# Ставим проверку ответа пользователя на команду /start - 60 сек
router.message.middleware(SlowpokeMiddleware(sleep_sec=60))


@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    """
    Обработчик команды /start.
    Приветствует пользователя и задает вопрос.
    """
    user = message.from_user.first_name
    await message.answer(f"Привет {user}! Как ты сегодня?", reply_markup=KEYBOARD)
    await state.set_state(LastMsg.msg)


@router.message(Command("help"))
async def help(message: types.Message):
    """
    Обработчик команды /help.
    Отправляет список доступных команд.
    """
    await message.answer(
        "Доступные команды: /start, /help, /echo, /photo, /inline, /start_fsm"
    )


@router.message(Command("echo"))
async def echo(message: types.Message):
    """
    Обработчик команды /echo.
    Отправляет обратно текст, который пользователь отправил после команды.
    """
    if len(message.text) > len("/echo "):
        await message.answer(message.text[len("/echo ") :])
    else:
        await message.answer("Пожалуйста, введите текст после команды /echo.")


@router.message(Command("inline"))
async def inline(message: types.Message):
    """
    Обработчик команды /inline.
    Отправляет inline клавиатуру для выбора опций.
    """
    await message.answer("Сделайте выбор:", reply_markup=INLINE_KEYBOARD)


@router.callback_query(ChoiceCallback.filter())
async def choice_callback(
    callback_query: types.CallbackQuery, callback_data: ChoiceCallback
):
    """
    Обработчик callback данных от inline кнопок.
    Отправляет сообщение с выбранной опцией.
    """
    option = callback_data.option
    if option == "1":
        await callback_query.message.answer("Вы выбрали Выбор 1")
    elif option == "2":
        await callback_query.message.answer("Вы выбрали Выбор 2")
    await callback_query.answer()


@router.message(Command("start_fsm"))
async def start_fsm(message: types.Message, state: FSMContext):
    """
    Обработчик команды /start_fsm.
    Запускает Finite State Machine (FSM) для сбора данных от пользователя.
    """
    await message.answer("Как вас зовут?")
    await state.set_state(Form.name)


@router.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    """
    Обработчик состояния Form.name.
    Запрашивает возраст пользователя после получения его имени.
    """
    await state.update_data(name=message.text)
    await message.answer("Сколько вам лет?")
    await state.set_state(Form.age)


@router.message(Form.age)
async def process_age(message: types.Message, state: FSMContext):
    """
    Обработчик состояния Form.age.
    Выводит собранные данные и завершает FSM.
    """
    await state.update_data(age=message.text)
    user_data = await state.get_data()
    await message.answer(
        f"Ваше имя: {user_data['name']}, ваш возраст: {user_data['age']}"
    )
    await state.clear()


@router.message(Command("photo"))
async def inline(message: types.Message):
    """
    Обработчик команды /photo.
    Запрашивает у пользователя отправить фотографию.
    """
    await message.answer("Пришлите фото, а мы пришлем вам его размеры!")


@router.message(F.photo)
async def handle_photo(message: types.Message):
    """
    Обработчик получения фотографии.
    Возвращает размеры изображения.
    """
    photo = message.photo[-1]
    await message.answer(f"Размер изображения: {photo.width} x {photo.height} пикселей")


@router.message()
async def handle_message(message: types.Message, state: FSMContext):
    """
    Обработчик всех остальных сообщений.
    Сбрасывает состояние FSM.
    """
    await state.set_state(None)
