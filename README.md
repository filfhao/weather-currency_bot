# Telegram Weather & Currency Bot

A Telegram bot for checking the weather and currency exchange rates.

## What can the bot do?

* 🌤 Check the weather in a city
* 💱 Get currency exchange rates
* 🎛️ Use buttons to choose an option
* ✉️ Contact the bot owner
* 💬 Work in private chats and groups

## Built with

* Python
* python-telegram-bot
* python-dotenv
* Weather API
* Currency API

## Files

* `main.py` — starts the bot
* `handlers.py` — bot commands and messages
* `services.py` — weather and currency API requests
* `responses.py` — bot responses
* `keyboard.py` — buttons and keyboards
* `config.py` — bot configuration

## How to run

Clone the repository and install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
TOKEN=your_telegram_bot_token
API_WEATHER=your_weather_api_key
```

Then open `config.py` and change the bot username:

```python
BOT_USERNAME = '@YourBotUsername'
```

Run the bot:

```bash
python main.py
```

Don't upload your `.env` file or share your API keys.

## About

This is one of my Python projects where I practiced working with Telegram bots, APIs, asynchronous code and Git/GitHub.
