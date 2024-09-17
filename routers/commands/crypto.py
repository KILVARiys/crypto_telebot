from aiogram import Router, types, F
from aiogram.filters import Command

from keybords.crypto_keybords import ButtonText, get_crypto_kb
from keybords.tasks_kb import tasks_actions_kb

router = Router(name=__name__)

@router.message(Command('crypto', prefix='!/'))
async def handler_info_command(message: types.Message):
    await message.answer(
        text='Выберите интересующую вас криптовалюту',
        reply_markup = get_crypto_kb(),
    )

@router.message(F.text == ButtonText.BTC)
async def hande_btc(message: types.Message):
    markup = tasks_actions_kb()
    await message.answer(
        text='Биткоин:',
        reply_markup=markup,
    )