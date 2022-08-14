import requests
import telebot
import re
import json
import time
from telebot import apihelper, types


with open('C:\\Users\zav\PycharmProjects\pythonProject\curs_tg_bot\config.json') as f:
    templates = json.load(f)
    tg_bot_token = templates["tg_bot_token"]
    coin_token = templates["coin_token"]

with open("C:\\Users\zav\PycharmProjects\pythonProject\curs_tg_bot\symbol_all.json", "r", encoding="utf-8") as fn:
    temp = json.load(fn)

bot = telebot.TeleBot(tg_bot_token)

reg = []


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Наберите команду /help, /menu')


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id, f"Введите пример: '/btc 10'\n {', '.join(temp)} ")
    elif message.text == "/menu":
        keyboard = [
            [
                types.InlineKeyboardButton(text='USD', callback_data='USD'),
                types.InlineKeyboardButton(text='EUR', callback_data='EUR'),
                types.InlineKeyboardButton(text='RUB', callback_data='RUB'),
                types.InlineKeyboardButton(text='JPY', callback_data='JPY'),
            ],
            [types.InlineKeyboardButton(text='CNY', callback_data='CNY'),
             types.InlineKeyboardButton(text='KRW', callback_data='KRW'),
             types.InlineKeyboardButton(text='TRY', callback_data='TRY'),
             types.InlineKeyboardButton(text='IRR', callback_data='IRR'),
            ],
        ]
        reply_markup = types.InlineKeyboardMarkup(keyboard)
        bot.send_message(message.from_user.id, text='Выбери курс валют', reply_markup=reply_markup)
    else:
        coin_list = re.findall(r'\d+', message.text)
        coin_int = int(coin_list[0]) if coin_list else 1
        symbol = "".join(re.findall(r'[a-zA-Z]', message.text))
        reg1 = reg if reg else ["RUB"]
        regist = get_url(reg1, symbol, temp)
        bot.send_message(message.chat.id, get_course(message, coin_int, symbol.upper(), regist))


# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "USD":
        reg.append(call.data)
        bot.send_message(call.from_user.id, text=f'Выбрана валюта {call.data}')
    elif call.data == "EUR":
        reg.append(call.data)
        bot.send_message(call.from_user.id, text=f'Выбрана валюта {call.data}')
    elif call.data == "RUB":
        reg.append(call.data)
        bot.send_message(call.from_user.id, text=f'Выбрана валюта {call.data}')
    elif call.data == "JPY":
        reg.append(call.data)
        bot.send_message(call.from_user.id, text=f'Выбрана валюта {call.data}')
    elif call.data == "CNY":
        reg.append(call.data)
        bot.send_message(call.from_user.id, text=f'Выбрана валюта {call.data}')
    elif call.data == "KRW":
        reg.append(call.data)
        bot.send_message(call.from_user.id, text=f'Выбрана валюта {call.data}')
    elif call.data == "TRY":
        reg.append(call.data)
        bot.send_message(call.from_user.id, text=f'Выбрана валюта {call.data}')
    elif call.data == "IRR":
        reg.append(call.data)
        bot.send_message(call.from_user.id, text=f'Выбрана валюта {call.data}')


def get_url(reg, symbol, temp):
    param_list = {}
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/category'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': coin_token,
    }
    for i in range(len(reg)):
        parameters = {
            "id": "605e2ce9d41eae1066535f7c",
            'start': '1',
            'limit': '1000',
            'convert': reg[i]
        }
        time.sleep(1)
        #  proxies=proxies
        response = requests.get(url, headers=headers, params=parameters)
        time.sleep(1)
        data = json.loads(response.text)
        param = data["data"]["coins"]
        param_list[reg[i]] = data
        for j in range(len(param)):
            if param[j]["symbol"] not in temp:
                temp.append(f'/{param[j]["symbol"]}')
                with open("C:\\Users\zav\PycharmProjects\pythonProject\curs_tg_bot\symbol_all.json", "w", encoding="utf-8") as f:
                    f.write(json.dumps(temp))
            if symbol.upper() in param[j]["symbol"]:
                param_list[reg[i]][param[j]["symbol"]] = {
                    "price": int(param[i]['quote'][reg[i]]['price']),
                    "volume_24h": int(param[j]['quote'][reg[i]]['volume_24h']),
                    "volume_change_24h": int(param[j]['quote'][reg[i]]['volume_change_24h']),
                    "percent_change_1h": param[j]['quote'][reg[i]]['percent_change_1h'],
                    "percent_change_24h": param[j]['quote'][reg[i]]['percent_change_24h'],
                }

    return param_list

@bot.message_handler(content_types=["text"])
def get_course(message, coin, symbol, regist):
    try:
        sp = {}
        source = "{:,d}"

        for key, value in regist.items():
            val = value.get(symbol)
            price = source.format(round(val['price'] * coin, 4))
            volume_24h = source.format(round(val['volume_24h'] * coin, 4))
            volume_change_24h = source.format(round(val['volume_change_24h'] * coin, 4))
            percent_change_1h = round(val['percent_change_1h'], 2)
            percent_change_24h = round(val['percent_change_24h'], 2)

            sp[key] = {
                "name": f"{list(value)[2]} {key}: {price}",
                "volume_24h": f"Объёма торгов за 24h: {volume_24h}",
                "volume_change_24h": f"Изменение объёма торгов за 24h: {volume_change_24h}",
                "percent_change_1h": f"Проценты за 1h: {percent_change_1h}%",
                "percent_change_24h": f"Проценты за 24h: {percent_change_24h}%",
            }
            bot.send_message(message.chat.id, '\n'.join([
                sp[key]["name"],
                sp[key]["volume_24h"],
                sp[key]["volume_change_24h"],
                sp[key]["percent_change_1h"],
                sp[key]["percent_change_24h"],
            ]))
    except:
        return ("\U00002620 Что то пошло не так \U00002620")


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)

