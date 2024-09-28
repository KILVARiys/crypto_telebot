from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keybords.tasks_kb import tasks_actions_kb, get_crypto_kb
from handlers.parser import check_price_coin
from sqlite_tasks import ent_info_db, give_tasks, del_info_db

router = Router(name=__name__)

# Хранение задач
tasks = []

class TaskStates(StatesGroup):
    waiting_for_crypto_title = State()
    waiting_for_price = State()
    waiting_for_task_number = State()

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
    async def handle_coin_callback(callback_query: types.CallbackQuery, state: FSMContext):
        coin = callback_query.data
        await state.update_data(crypto_name=coin)  # Сохраняем название криптовалюты в состоянии
        await callback_query.message.answer(
            text=f'Нынешняя цена данной криптовалюты: {check_price_coin(crypto_name=coin)}\n'
                 f'Если желаете установить цену то введите число(Вводите в формате USD): '
        )
        await state.set_state(TaskStates.waiting_for_price)  # Переход к ожиданию цены

    @router.message()  # Обработчик для получения цены
    async def handle_price_input(message: types.Message, state: FSMContext):
        price = message.text  # Получаем цену от пользователя
        data = await state.get_data()  # Получаем сохраненные данные из состояния
        crypto_name = data.get('crypto_name')  # Извлекаем название криптовалюты

        # Проверка, является ли цена числом
        if price.isdigit():
            if crypto_name:
                ent_info_db(user_id=message.from_user.id, currency=crypto_name, price=price)
                await message.answer(f'Вы успешно установили цену: {price} USD для {crypto_name}')
            else:
                await message.answer('Ошибка: название криптовалюты не найдено.')
        else:
            await message.answer('Ошибка: пожалуйста, введите корректную цену в формате USD.')

@router.callback_query(F.data == 'del_quets')
async def del_tasks_check_number(call: CallbackQuery, state: FSMContext):
    await state.set_state(TaskStates.waiting_for_task_number)  # Переход в новое состояние
    await call.message.answer(
        text='Напишите номер задачи, которую хотите убрать: ',
    )

@router.message(StateFilter(TaskStates.waiting_for_task_number))  # Обработчик для получения номера задачи
async def del_task(message: types.Message, state: FSMContext):
    task_id = message.text  # Получаем номер задачи от пользователя

    # Проверка, является ли task_id числом
    if task_id.isdigit():
        result = del_info_db(user_id=message.from_user.id, task_id=int(task_id))
        if result:  # Если удаление прошло успешно
            await message.answer(f'Задача номер {task_id} не найдена.')
        else:
            await message.answer(f'Задача номер {task_id} успешно удалена.')
    else:
        await message.answer('Ошибка: пожалуйста, введите корректный номер задачи.')

    await state.clear()  # Очистка состояния после завершения работы

@router.callback_query(F.data == 'check_quets')
async def check_tasks(call: CallbackQuery):
    await call.message.answer(
        text='Ваши задачи:',
    )
    user_tasks = give_tasks(user_id=call.from_user.id)
    for task in user_tasks:
        await call.message.answer(f"Номер задачи: {task[0]}, Монета: {task[2]}, Цена: {task[3]}")
