from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
# token = os.getenv('BOT_KEY')
from handlers import register_user_handlers

bot = Bot('5012407051:AAG_TsNKPpzj8D6Vc9XKMKxzwG9fFj1n_24')
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

register_user_handlers(dp)
executor.start_polling(dispatcher=dp, skip_updates=True)
