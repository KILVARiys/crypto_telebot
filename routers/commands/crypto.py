from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keybords.tasks_kb import tasks_actions_kb, get_crypto_kb

router = Router(name=__name__)

# Хранение задач
tasks = []

class TaskStates(StatesGroup):
    waiting_for_crypto_title = State()
    waiting_for_price = State()

@router.message(Command('crypto', prefix='!/'))
async def handler_info_command(message: types.Message):
    markup = tasks_actions_kb()
    await message.answer(
        text='Выберите интересующую вас функцию',
        reply_markup=markup,
    )

@router.callback_query(F.data == 'add_quets')
async def add_tasks(call: CallbackQuery, state: FSMContext):
    await state.set_state(TaskStates.waiting_for_crypto_title)
    await call.message.answer(
        text="Выберите криптовалюту:",
        reply_markup=get_crypto_kb(),
    )

@router.callback_query(lambda call: call.data in {'coin_btc', 'coin_eth', 'coin_ltc'})
async def handle_coin_callback(callback_query: types.CallbackQuery):
    coin = callback_query.data
    await callback_query.message.answer(
        text='Нынешняя цена данной криптовалюты: \n'
             'Если желаете установить цену введите /setprice'
    )
    return coin

@router.message(Command('setprice', prefix='!/'))
async def handle_setprice(message: types.Message):
    await message.answer('Введите желаемую цену в формате USD: ')

@router.message()  # Обработчик для получения цены
async def handle_price_input(message: types.Message):
    price = message.text  # Получаем цену от пользователя
    # Здесь вы можете добавить логику для обработки полученной цены
    await message.answer(f'Вы успешно установили цену: {price} USD')
    return price

@router.callback_query(F.data == 'del_quets')
async def del_tasks(call: CallbackQuery):
    await call.message.answer(
        text='Удаляю задачу'
    )