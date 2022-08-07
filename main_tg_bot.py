import requests
import telebot
import re
import json
import time
# from telebot import apihelper

# proxies = {"https": "hqproxyusr.avp.ru:8080", "http": "hqproxyusr.avp.ru:8080"}
# apihelper.proxy = proxies

with open('config.json') as f:
    templates = json.load(f)
    tg_bot_token = templates["tg_bot_token"]
    coin_token = templates["coin_token"]

bot = telebot.TeleBot(tg_bot_token)

# wikipedia.set_lang("ru")

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Наберите команду /help')


@bot.message_handler(content_types=["text"])
def handle_text(message):
    with open("symbol_usd.json", "r", encoding="utf-8") as fn:
        templates = json.load(fn)

    if message.text == "/help":
        bot.send_message(message.from_user.id, f"Введите пример: '/btc 10'\n {', '.join(templates.keys())} ")
    else:
        coin_int = re.findall(r'\d+', message.text)
        symbol = "".join(re.findall(r'[a-zA-Z]', message.text))
        bot.send_message(message.chat.id, get_course(int(coin_int[0]), symbol))


def percent(new: int, old: int):
    return round((new - old) / old * 100, 2)

def get_symbol(message: list, parameter):
    symbol = []
    value = {}

    for i in range(len(message)):
        symbol.append(message[i]["symbol"])
        value[message[i]["symbol"]] = {
            "price": int(message[i]['quote'][parameter]['price']),
            "volume_24h": int(message[i]['quote'][parameter]['volume_24h']),
            "volume_change_24h": int(message[i]['quote'][parameter]['volume_change_24h']),
            "percent_change_1h": message[i]['quote'][parameter]['percent_change_1h'],
            "percent_change_24h": message[i]['quote'][parameter]['percent_change_24h'],
        }
    if parameter == "RUB":
        with open("symbol_rub.json", 'w') as f:
            f.write(json.dumps(value))
    else:
        with open("symbol_usd.json", 'w') as f:
            f.write(json.dumps(value))

    return symbol


def get_course(coin, symbol):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/category'
    parameters_usd = {
        "id": "605e2ce9d41eae1066535f7c",
        'start': '1',
        'limit': '1000',
        'convert': 'USD'
    }
    parameters_rub = {
        "id": "605e2ce9d41eae1066535f7c",
        'start': '1',
        'limit': '1000',
        'convert': 'RUB'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': coin_token,
    }

    try:
        #  proxies=proxies
        response_rub = requests.get(url, headers=headers, params=parameters_rub)
        time.sleep(1)
        response_usd = requests.get(url, headers=headers, params=parameters_usd)
        time.sleep(1)
        data_rub = json.loads(response_rub.text)
        data_usd = json.loads(response_usd.text)
        get_symbol(data_rub["data"]["coins"], parameters_rub['convert'])
        symbols = get_symbol(data_usd["data"]["coins"], parameters_usd['convert'])

        with open("symbol_rub.json", "r", encoding="utf-8") as f:
            templates_rub = json.load(f)

        with open("symbol_usd.json", "r", encoding="utf-8") as fn:
            templates_usd = json.load(fn)
        sp = {}
        source = "{:,d}"
        for key, value in templates_rub.items():
            if key == symbol.upper():
                price = source.format(round(value['price'] * coin, 4))
                # volume_24h = source.format(round(value['volume_24h'] * coin, 4))
                # volume_change_24h = source.format(round(value['volume_change_24h'] * coin, 4))
                # percent_change_1h = round(value['percent_change_1h'], 2)
                # percent_change_24h = round(value['percent_change_24h'], 2)

                sp["RUB"] = {
                    "name": f"{key} {parameters_rub['convert']}: {price}",
                    # "volume_24h": f"Значение 24h: {volume_24h}",
                    # "volume_change_24h": f"Значение обновлено 24h: {volume_change_24h}",
                    # "percent_change_1h": f"Проценты 1h: {percent_change_1h}%",
                    # "percent_change_24h": f"Проценты 24h: {percent_change_24h}%",
                }
        for key, value in templates_usd.items():
            if key == symbol.upper():
                price = source.format(round(value['price'] * coin, 4))
                volume_24h = source.format(round(value['volume_24h'] * coin, 4))
                volume_change_24h = source.format(round(value['volume_change_24h'] * coin, 4))
                percent_change_1h = round(value['percent_change_1h'], 2)
                percent_change_24h = round(value['percent_change_24h'], 2)

                sp["USD"] = {
                    "name": f"{key} {parameters_usd['convert']}: {price}",
                    "volume_24h": f"Объёма торгов за 24h: {volume_24h}",
                    "volume_change_24h": f"Изменение объёма торгов за 24h: {volume_change_24h}",
                    "percent_change_1h": f"Проценты за 1h: {percent_change_1h}%",
                    "percent_change_24h": f"Проценты за 24h: {percent_change_24h}%",
                }

        return "\n".join(
            (sp["RUB"]["name"],
            sp["USD"]["name"],
            sp["USD"]["volume_24h"],
            sp["USD"]["volume_change_24h"],
            sp["USD"]["percent_change_1h"],
            sp["USD"]["percent_change_24h"],)
        )

    except:
        return ("\U00002620 Что то пошло не так \U00002620")


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)

