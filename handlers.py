from telegram import Update
from config import BOT_USERNAME
from telegram.ext import ContextTypes
from responses import handle_response
from services import get_weather, get_currency_rate
from keyboard import main_keyboard, get_weather_text, get_currency_text, get_contact_text, contact_button

#Commands
async def start_command(update, context):
    await update.message.reply_text(
        "👋 Hello! Nice to meet you!\n\n"
        "What would you like to do?",
        reply_markup=main_keyboard
    )

async def help_command(update, context):
    await update.message.reply_text(
        "Hey! 👋 Here's what I can do:\n\n"
        "🌤 Weather — get the current weather in any city\n"
        "💱 Currency — check exchange rates\n"
        "✉️ Contact the owner — get in touch with me\n\n"
        "Just choose an option from the keyboard below! 😊")

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
    if text == get_weather_text:
        await weather_command(update, context)
        return
    if text == get_currency_text:
        await currency_command(update, context)
        return
    if text == get_contact_text:
        await update.message.reply_text(
            "If you have any questions, feel free to contact me:",
            reply_markup=contact_button
        )
        return
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    if await handle_waiting(
        update,
        context,
        "waiting_weather",
        get_weather,
        "❌ City is not found. Try again"
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
            print(new_text)
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    print("Bot:", response)
    await update.message.reply_text(response)

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        city = " ".join(context.args)
        weather = get_weather(city)
        await update.message.reply_text(weather)
    else:
        context.user_data["waiting_weather"] = True
        await update.message.reply_text("🏙️ Enter the name of the city:")

async def currency_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        currency = " ".join(context.args)
        rate = get_currency_rate(currency)
        await update.message.reply_text(rate)
    else:
        context.user_data["waiting_currency"] = True
        await update.message.reply_text("🪙Enter the currency name:")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


