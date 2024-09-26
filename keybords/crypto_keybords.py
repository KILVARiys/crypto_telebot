# from aiogram.types import (
#     KeyboardButton,
#     ReplyKeyboardMarkup,
# )
#
# class ButtonText:
#     BTC = 'Bitcoin|USD'
#     ETH = 'Ethereum|USD'
#     LTC = 'Litecoin|USD'
#
# def get_crypto_kb() -> ReplyKeyboardMarkup:
#     button_btc = KeyboardButton(text=ButtonText.BTC)
#     button_eth = KeyboardButton(text=ButtonText.ETH)
#     button_ltc = KeyboardButton(text=ButtonText.LTC)
#
#     buttons_first_row = [button_btc]
#     buttons_second_row = [button_eth]
#     buttons_thirt_row = [button_ltc]
#
#     markup = ReplyKeyboardMarkup(
#         keyboard=[buttons_first_row, buttons_second_row, buttons_thirt_row],
#         # Выравнивает кнопку по размеру текста
#         resize_keyboard=True,
#     )
#     return markup
#
