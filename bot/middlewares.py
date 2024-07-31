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
        # Проверяем, является ли сообщение командой /start
        if event.text.startswith("/start"):
            # Устанавливаем время задержки в контекст
            data["sleep_sec"] = self.sleep_sec

            # Вызываем обработчик события
            result = await handler(event, data)

            # Задержка на указанное количество секунд
            await asyncio.sleep(self.sleep_sec)

            # Проверяем состояние FSM
            state = data.get("state")
            if state:
                current_state = await state.get_state()
                # Если состояние все еще LastMsg.msg, значит пользователь не ответил
                if current_state == LastMsg.msg:
                    await event.answer("Вы забыли ответить")
        else:
            # Если сообщение не команда /start, просто вызываем обработчик
            result = await handler(event, data)
        return result
