from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keybords.crypto_keybords import ButtonText, get_crypto_kb
from keybords.tasks_kb import tasks_actions_kb

router = Router(name=__name__)

# Хранение задач
tasks = []

class TaskStates(StatesGroup):
    waiting_for_crypto_title = State()
    waiting_for_price = State()

@router.message(Command('crypto', prefix='!/'))
async def handler_info_command(message: types.Message):
    await message.answer(
        text='Выберите интересующую вас криптовалюту',
        reply_markup=get_crypto_kb(),
    )

@router.message(F.text == ButtonText.BTC)
async def handle_btc(message: types.Message):
    markup = tasks_actions_kb()
    await message.answer(
        text='Биткоин:',
        reply_markup=markup,
    )

@router.callback_query(F.data == 'add_quets')
async def add_tasks(call: CallbackQuery, state: FSMContext):
    await state.set_state(TaskStates.waiting_for_crypto_title)
    await call.message.answer("Введите название криптовалюты [BTC]|[ETH]|[LTC]:")

@router.callback_query(F.state.state)
async def process_crypto_title(call: CallbackQuery, state: FSMContext):
    title = call.message.text  # Используется текст сообщения, обновите при необходимости
    await state.update_data(title=title)  # Сохраняем заголовок
    await state.set_state(TaskStates.waiting_for_price)
    await call.message.answer("Введите ожидаемую сумму в USD:")

@router.message(F.state.state)  # Убедитесь, что state правильный
async def process_price(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    title = user_data.get('title')
    price = message.text  # Получаем сумму

    task = {'title': title, 'price': price}
    tasks.append(task)

    await message.answer(f'Задача добавлена: {title} с ценой {price}.')
    await state.clear()  # Очищаем состояние после завершения добавления задания

@router.callback_query(F.data == 'del_quets')
async def del_tasks(call: CallbackQuery):
    await call.message.answer(
        text='Удаляю задачу'
    )