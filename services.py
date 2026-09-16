from config import API_WEATHER
import requests
import time
import pprint
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_WEATHER}&units=metric&lang=ua"
    try:
        response = requests.get(url,timeout=5)
        data = response.json()
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return "❌ Failed to connect to the weather server"
    if response.status_code !=200:
        return "❌ City is not found. Try again"
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    weather_id = data["weather"][0]["id"]
    if weather_id == 800:
        emoji =  "🔆"
    else:
        category = weather_id//100
        match(category):
            case 2: emoji =  "⛈️"
            case 3: emoji =  "🌧"
            case 5: emoji =  "🌧️"
            case 6: emoji =  "❄️"
            case 7: emoji =  "🌫️"
            case 8: emoji =  "☁️"
            case _: emoji =  "🌍"

    result = (
        f"Weather\n"
        f"📍City: {city}\n"
        f"🌡Temperature: {temp}℃\n"
        f"{emoji} {desc.capitalize()}\n"
        f"💧 Humidity: {humidity}%\n"
        f"༄ Wind: {wind} м/с\n"
    )
    return result
CACHE_DATA = None
CACHE_TIME = 0

def update_currency_cache():
    global CACHE_DATA, CACHE_TIME
    url = "https://api.monobank.ua/bank/currency"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return "❌ Failed to connect to the server"
    if "errCode" in data:
        return "❌ The currency exchange rate service is temporarily unavailable. Please try again in a few minutes"
    CACHE_DATA = data
    CACHE_TIME = time.time()
    return data

def get_currency_rate(currency:str):
    currency_code_uah = 980
    currency_code = None
    CURRENCIES = {
        "USD": {
            "code": 840,
            "emoji": "💵",
            "names": ["usd", "долар", "доллар", "dollar"]
        },
        "EUR": {
            "code": 978,
            "emoji": "💶",
            "names": ["eur", "євро", "евро", "euro"]
        },
        "GBP": {
            "code": 826,
            "emoji": "💷",
            "names": ["gbp", "фунт", "фунт стерлінгів", "фунт стерлингов", "sterling", "pound"]
        },
        "PLN": {
            "code": 985,
            "emoji": "🇵🇱",
            "names": ["pln", "злотий", "злотый", "zloty"]
        },
        "JPY": {
            "code": 392,
            "emoji": "💴",
            "names": ["jpy", "єна", "иена", "yen", "ена"]
        }
    }

    if not CACHE_DATA or time.time()-CACHE_TIME > 300:
        print("Updating cache...")
        data = update_currency_cache()
        if isinstance(data,str):
            return data
    else:
        print("Using cache")
        data = CACHE_DATA

    for currency_name, info in CURRENCIES.items():
        if currency.lower() in info["names"]:
            currency_code = info["code"]
            currency_emoji = info["emoji"]
            selected_currency = currency_name
            break
    if currency_code is None:
        return "❌ Currency not supported. Try again! 😇"



    for item in data:
        if item['currencyCodeA'] == currency_code and item["currencyCodeB"] == currency_code_uah:
            if item.get("rateCross"):
                currency_cross = item["rateCross"]
                return (
                    f"💱 Exchange Rate\n"
                    f"{currency_emoji} Currency: {selected_currency}\n"
                    f"📈 Rate:{currency_cross:.1f} UAH"
                )
            else:
                currency_buy = item["rateBuy"]
                currency_sell = item["rateSell"]
                return (
                    f"💱 Exchange Rate\n"
                    f"{currency_emoji} Currency: {selected_currency}\n"
                    f"🟢 Buy:{currency_buy:.1f} UAH\n"
                    f"🔴 Sell:{currency_sell:.1f} UAH \n"
                )
    return "❌ Currency rate not found."


