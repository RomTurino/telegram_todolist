from config import TOKEN
from constants import *
from database_module import read_tasks
from interrupt import cancel, endpoint, wrong_message
from start_menu import main_menu, start
from task_create import (add_task, handle_date, handle_hour, handle_minute,
                         handle_task_text, save_result)
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler,
                          Updater)
from telegram_bot_calendar import DetailedTelegramCalendar

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

add_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(f"^{CREATE}$"), add_task)],
    states={
        # CallbackQueryHandler(handle_task_text)
        TASK: [MessageHandler(Filters.text & ~Filters.command, handle_task_text)],
        DATE: [CallbackQueryHandler(handle_date, DetailedTelegramCalendar.func)],
        HOUR: [CallbackQueryHandler(handle_hour)],
        MINUTE: [CallbackQueryHandler(handle_minute)],
        RESULT: [CallbackQueryHandler(save_result)],
    },
    fallbacks=[CommandHandler("no", endpoint)],
)

contact_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        MENU: [MessageHandler(Filters.text, main_menu)],
        MENU_ITEMS: [
            MessageHandler(Filters.regex(f"^{READ}$"), read_tasks),
            add_handler,
            MessageHandler(Filters.text, wrong_message),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

dispatcher.add_handler(contact_handler)
print("started:", updater.bot.first_name)
updater.start_polling()
updater.idle()
