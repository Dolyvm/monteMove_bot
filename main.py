from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from admin_panel import register_admin_handlers
from handlers import register_user_handlers
from statistics.stats_functions import scheduler

bot = Bot(TOKEN)  # prod
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

register_user_handlers(dp)
register_admin_handlers(dp)

scheduler.start()
executor.start_polling(dispatcher=dp, skip_updates=True)
