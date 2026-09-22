from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

get_weather_text = "🌤 Weather"
get_currency_text = "💱 Currency"
get_contact_text = "✉️ Contact the owner"

main_keyboard = ReplyKeyboardMarkup(
    [
        [get_weather_text, get_currency_text],
        [get_contact_text]
    ],
    resize_keyboard=True
)

contact_button = InlineKeyboardMarkup([
    [InlineKeyboardButton(
        "💬 Open chat",
        url="https://t.me/filfhao"
    )]
])