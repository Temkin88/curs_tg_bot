"""
https://blogs.sap.com/2022/02/16/how-to-write-independent-unit-test-with-pytest-and-mock-techniques/
# run all tests
python -m pytest tests

# run single tests file
python -m pytest tests/test_calc.py

# run single tests case
python -m pytest tests/test_calc.py::test_add
"""
import time
import pytest
from curs_tg_bot.main_tg_bot import get_course, get_url, handle_text


temp = ["/BTC", "/ETH", "/XRP", "/FLOW", "/FIL", "/MKR", "/CELO", "/AR", "/ROSE", "/COMP", "/KEEP", "/RLY", "/YGG", "/OXT", "/HNS"]



def test_url(mocker):
    # m = mocker.patch("src.example.time.sleep", return_value=None)
    moc_now = mocker.patch("curs_tg_bot.main_tg_bot.get_url", return_value={
                    "price": int(123),
                    "volume_24h": int(123),
                    "volume_change_24h": int(123),
                    "percent_change_1h": "100",
                    "percent_change_24h": "100",
                })

    assert moc_now.return_value["price"] == 123
    assert moc_now.return_value["volume_24h"] == 123
    assert moc_now.return_value["volume_change_24h"] == 123
    assert moc_now.return_value["percent_change_1h"] == "100"
    assert moc_now.return_value["percent_change_24h"] == "100"
    assert type(moc_now.return_value["price"]) == int
    assert type(moc_now.return_value["volume_24h"]) == int
    assert type(moc_now.return_value["volume_change_24h"]) == int
    assert type(moc_now.return_value["percent_change_1h"]) == str
    assert type(moc_now.return_value["percent_change_24h"]) == str


def test_get_course(mocker):
    mocker_now = mocker.patch("curs_tg_bot.main_tg_bot.get_course", return_value={
                "name": f"BTC USD: {123}",
                "volume_24h": f"Объёма торгов за 24h: {12345}",
                "volume_change_24h": f"Изменение объёма торгов за 24h: {1234}",
                "percent_change_1h": f"Проценты за 1h: {30}%",
                "percent_change_24h": f"Проценты за 24h: {30}%",
            })

    assert mocker_now.return_value["name"] == "BTC USD: 123"
    assert mocker_now.return_value["volume_24h"] == "Объёма торгов за 24h: 12345"
    assert mocker_now.return_value["volume_change_24h"] == "Изменение объёма торгов за 24h: 1234"
    assert mocker_now.return_value["percent_change_1h"] == "Проценты за 1h: 30%"
    assert mocker_now.return_value["percent_change_24h"] == "Проценты за 24h: 30%"


# def test_mock_api_call(mocker):
#     mock_requests = mocker.patch("requests.get")
#     mock_requests.return_value.ok = True
#     mock_requests.return_value.text = "Success"
#
#     schedule = get_url(["RUB"], "BTC", "temp")
#     mock_requests.assert_called_with('https://pro-api.coinmarketcap.com/v1/cryptocurrency/category')
#     assert mock_requests.return_value.text == "Success"



def test_course(mocker):
    mocker_now = mocker.patch("curs_tg_bot.main_tg_bot.handle_text", return_value="/help")
    assert mocker_now.return_value == "/help"


def test_menu(mocker):
    val = get_url(["RUB"], "BTC", temp)
    assert type(val["RUB"]) == dict
    assert type(val["RUB"]["BTC"]) == dict
    assert type(val["RUB"]["BTC"]["price"]) == int
    assert type(val["RUB"]["BTC"]['volume_24h']) == int
    assert type(val["RUB"]["BTC"]['volume_change_24h']) == int
    assert type(val["RUB"]["BTC"]['percent_change_1h']) == float
    assert type(val["RUB"]["BTC"]['percent_change_24h']) == float