# https://www.coingecko.com/en/api/documentation
# https://docs.coincap.io/
# https://pro.coinmarketcap.com/account

import requests
import datetime
import json
from pprint import pprint

proxies = {"https": "hqproxyusr.avp.ru:8080", "http": "hqproxyusr.avp.ru:8080"}


with open('config.json') as f:
    templates = json.load(f)
    tg_bot_token = templates["tg_bot_token"]
    coin_token = templates["coin_token"]

# def percent(new: int, old: int):
#     return round((new - old) / old * 100, 2)

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


def get_course(coin):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/trending/latest'
    # url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/category'
    parameters_usd = {
        "id": "605e2ce9d41eae1066535f7c",
        'start': '1',
        'limit': '1000',
        'convert': 'USD'
    }
    # parameters_rub = {
    #     "id": "605e2ce9d41eae1066535f7c",
    #     'start': '1',
    #     'limit': '1000',
    #     'convert': 'RUB'
    # }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': coin_token,
    }

    try:
        #  params=parameters
        # response_rub = requests.get(url, headers=headers, params=parameters_rub, proxies=proxies)
        # response_rub = requests.get(url, headers=headers, proxies=proxies)
        # data_rub = json.loads(response_rub.text)
        response_usd = requests.get(url, headers=headers, params=parameters_usd, proxies=proxies)
        data_usd = json.loads(response_usd.text)
        # get_symbol(data_rub["data"]["coins"], parameters_rub['convert'])
        # symbol = get_symbol(data_usd["data"]["coins"], parameters_usd['convert'])
        pprint(data_usd)

        with open("symbol_rub.json", "r", encoding="utf-8") as f:
            templates_rub = json.load(f)

        with open("symbol_usd.json", "r", encoding="utf-8") as f:
            templates_usd = json.load(f)

        for key, value in templates_rub.items():
            a =1
            usd_price = round(value['price'] * coin, 4)
            usd_volume_24h = round(value['volume_24h'] * coin, 4)
            usd_volume_change_24h = round(value['volume_change_24h'] * coin, 4)
            usd_percent_change_1h = round(value['percent_change_1h'], 2)
            usd_percent_change_24h = round(value['percent_change_24h'], 2)

            print(
                  f"{key} {parameters_rub['convert']}: {usd_price}\n"
                  f"{key} {parameters_rub['convert']}: {usd_volume_24h}\n"
                  f"{key} {parameters_rub['convert']}: {usd_volume_change_24h}\n"
                  f"{key} {parameters_rub['convert']}: {usd_percent_change_1h}%\n"
                  f"{key} {parameters_rub['convert']}: {usd_percent_change_24h}%\n"
                  )
        for key, value in templates_usd.items():
            a =1
            usd_price = round(value['price'] * coin, 4)
            usd_volume_24h = round(value['volume_24h'] * coin, 4)
            usd_volume_change_24h = round(value['volume_change_24h'] * coin, 4)
            usd_percent_change_1h = round(value['percent_change_1h'], 2)
            usd_percent_change_24h = round(value['percent_change_24h'], 2)

            print(
                  f"{key} {parameters_usd['convert']}: {usd_price}\n"
                  f"{key} {parameters_usd['convert']}: {usd_volume_24h}\n"
                  f"{key} {parameters_usd['convert']}: {usd_volume_change_24h}\n"
                  f"{key} {parameters_usd['convert']}: {usd_percent_change_1h}%\n"
                  f"{key} {parameters_usd['convert']}: {usd_percent_change_24h}%\n"
                  )
    except:
        return ("\U00002620 Что то пошло не так \U00002620")


if __name__ == '__main__':
    coin = str(input("Введите курс: "))
    get_course(int(coin))
