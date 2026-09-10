from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TOKEN
from handlers import start_command, help_command, custom_command, handle_message, weather_command, currency_command, error
from services import get_weather, get_currency_rate


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    print(get_currency_rate("gbp"))
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('custom',custom_command))
    app.add_handler(CommandHandler('weather',weather_command))
    app.add_handler(CommandHandler('currency',currency_command))



    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)

    #Polling
    print('Polling...')
    app.run_polling(poll_interval=1)


