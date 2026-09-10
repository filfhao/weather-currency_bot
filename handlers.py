from telegram import Update
from config import BOT_USERNAME
from telegram.ext import ContextTypes
from responses import handle_response
from services import get_weather, get_currency_rate

#Commands
async def start_command(update, context):
    await update.message.reply_text('Hello! Nice to meet you!')

async def help_command(update, context):
    await update.message.reply_text('I`m here to help you with your routine. Choose a command so I can help you')

async def custom_command(update, context):
    await update.message.reply_text('Custom command!')

#Responses

async def handle_waiting(update, context, waiting_key, handler, error_text):
    text = update.message.text

    if context.user_data.get(waiting_key):
        if text.lower() in ["cancel", "отмена", "відміна"]:
            context.user_data.pop(waiting_key)
            await update.message.reply_text("❌ Запит скасовано")
            return True

        item = handler(text)
        await update.message.reply_text(item)

        if item != error_text:
            context.user_data.pop(waiting_key, None)

        return True

    return False
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    if await handle_waiting(
        update,
        context,
        "waiting_weather",
        get_weather,
        "❌Місто не знайдено. Спробуй ще раз"
    ):
        return
    if await handle_waiting(
        update,
        context,
        "waiting_currency",
        get_currency_rate,
        "❌ Currency not supported. Try again! 😇"
    ):
        return

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    print("Bot:", response)
    await update.message.reply_text(response)

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = " ".join(context.args)
    if city:
        weather = get_weather(city)
        await update.message.reply_text(weather)
    else:
        context.user_data["waiting_weather"] = True
        await update.message.reply_text("🏙️Введіть назву міста:")

async def currency_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currency = " ".join(context.args)
    if currency:
        rate = get_currency_rate(currency)
        await update.message.reply_text(rate)
    else:
        context.user_data["waiting_currency"] = True
        await update.message.reply_text("🪙Введіть назву валюти:")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


