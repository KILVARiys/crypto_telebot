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
        reply_markup = get_crypto_kb(),
    )

@router.message(F.text == ButtonText.BTC)
async def hande_btc(message: types.Message):
    markup = tasks_actions_kb()
    await message.answer(
        text='Биткоин:',
        reply_markup=markup,
    )

@router.callback_query(F.data == 'add_quets')
async def add_tasks(call: CallbackQuery):
    await call.message.answer("Введите название криптовалюты [BTC]|[ETH]|[LTC]:")
    await TaskStates.waiting_for_crypto_title.set()

    await call.message.answer("Введите ожидаемую сумму в USD:")
    await TaskStates.waiting_for_price.set()

@router.callback_query(F.data == 'del_quets')
async def del_tasks(call: CallbackQuery):
    await call.message.answer(
        text='Удаляю задачу'
    )

@router.message(state=TaskStates.waiting_for_description)
async def process_description(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    title = user_data['title']
    description = message.text

    task = {'title': title, 'description': description}
    tasks.append(task)

    await message.answer(f'Задача добавлена: {title}.')
