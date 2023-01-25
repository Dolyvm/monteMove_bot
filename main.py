from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from admin_panel import register_admin_handlers
from handlers import register_user_handlers
from statistics.stats_functions import scheduler

# bot = Bot('5626261222:AAHKJo2DzuU5vpMJuBQspVbPJmOge6nJaJs')  # prod
bot = Bot("5012407051:AAG_TsNKPpzj8D6Vc9XKMKxzwG9fFj1n_24")  # test
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

register_user_handlers(dp)
register_admin_handlers(dp)

scheduler.start()
executor.start_polling(dispatcher=dp, skip_updates=True)
