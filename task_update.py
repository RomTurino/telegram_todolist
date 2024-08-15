from constants import MONTHS, TASK, TODO_DATE, TODO_TEXT, TODO_TIME
from database_module import get_all_tasks, read_tasks
from interrupt import delete_message
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext


def update_task(update: Update, context: CallbackContext):
    name = update.effective_user.full_name
    delete_message(update, context, end=1)
    read_tasks(update, context)
    update.message.reply_sticker(
        "CAACAgQAAxkBAAIPDWN-FI0ayXN81MJBalA0-27jCRtgAAJtlAACiLDJS5-sPYj-39D6pKwQ"
    )
    update.message.reply_text(f"Какое дело изменить, мастер {name}?")
    return TASK


def choose_action(update: Update, context: CallbackContext):
    number = update.message.text
    if not number.isdigit():
        update.message.reply_text("Вы ввели не число")
        return
    number = int(number) - 1
    filename = context.user_data["file"]
    task = get_all_tasks(filename)[number]
    keyboard = [TODO_TEXT, TODO_DATE, TODO_TEXT]
    markup = ReplyKeyboardMarkup(keyboard)
    todo_text, date, time = task
    year, month, day = str(date).split("-")
    update.message.reply_text(
        f"""
                                      To Do №{number}:
                                      {todo_text}
                                      Дедлайн: {day} {MONTHS[int(month)]} {year}
                                      {time}
                                      """
    )
    update.message.reply_text("Что хочешь поменять?", reply_markup=markup)
