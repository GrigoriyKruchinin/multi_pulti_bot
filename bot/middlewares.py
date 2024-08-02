import asyncio
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, types
from aiogram.fsm.context import FSMContext

from states import LastMsg


class SlowpokeMiddleware(BaseMiddleware):
    """
    Middleware для проверки ответа пользователя на команду /start.
    Задерживает обработку события на указанное количество секунд и проверяет,
    был ли дан ответ пользователем. Если ответа не было, отправляет уведомление.
    """

    def __init__(self, sleep_sec: int):
        """
        Инициализирует middleware с заданным временем задержки.

        :param sleep_sec: Количество секунд, на которое задерживается обработка события.
        """
        super().__init__()
        self.sleep_sec = sleep_sec

    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any],
    ) -> Any:
        """
        Основной метод middleware, который выполняет задержку и проверку ответа.

        :param handler: Обработчик, который будет вызван для обработки события.
        :param event: Сообщение Telegram.
        :param data: Дополнительные данные, переданные в контексте.
        :return: Результат выполнения обработчика.
        """
        # Проверяем, является ли сообщение командой /start и не является ли командой /start_fsm
        if event.text.startswith("/start") and event.text != "/start_fsm":
            # Устанавливаем время задержки в контекст данных
            data["sleep_sec"] = self.sleep_sec
            # Получаем состояние FSM из данных контекста
            state: FSMContext = data.get("state")

            if state:
                # Сбрасываем состояние и данные при новом вызове команды /start
                await state.clear()
                await state.update_data(notified=False)

            # Вызываем обработчик события
            result = await handler(event, data)
            # Задержка на указанное количество секунд
            await asyncio.sleep(self.sleep_sec)

            if state:
                # Получаем текущее состояние FSM
                current_state = await state.get_state()
                # Получаем данные FSM
                notified = await state.get_data()
                # Проверяем, если состояние равно LastMsg.msg и напоминание еще не отправлено
                if current_state == LastMsg.msg and not notified.get("notified", False):
                    # Отправляем напоминание пользователю
                    await event.answer("Вы забыли ответить")
                    # Обновляем данные FSM, устанавливая флаг напоминания
                    await state.update_data(notified=True)
        else:
            # Если сообщение не команда /start или команда /start_fsm, просто вызываем обработчик
            result = await handler(event, data)

        return result
