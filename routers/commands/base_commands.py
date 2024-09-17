from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown

router = Router(name=__name__)

# Обработка команды старт
@router.message(CommandStart())
async def handle_start(message: types.Message):
    url = 'https://indicator.ru/thumb/1360x0/filters:quality(75):no_upscale()/imgs/2019/08/13/13/3515290/a1ecb28bb786e47e966700e573595acc2f80885d.jpghttps://indicator.ru/thumb/1360x0/filters:quality(75):no_upscale()/imgs/2019/08/13/13/3515290/a1ecb28bb786e47e966700e573595acc2f80885d.jpg'

    await message.answer(
        text=f"{markdown.hide_link(url=url)}Привет, {markdown.hbold(message.from_user.full_name)}!\n"
             f"Напишите команду /info если не знаете для чего нужен данный бот!\n"
             f"Если знаете то напишите /crypto ",
        parse_mode=ParseMode.HTML,
    )

#Информация о боте
@router.message(Command('info', prefix='!/'))
async def handler_info_command(message: types.Message):
    await message.answer(
        text='Данный бот предназначен для мониторинга цены на криптовалюты интересующие польхзователя\n'
             'Как это работает?\n'
             '1: Вы выбираете нужную вам криптовалюту\n'
             '2: Назначаете ей интересующую вас цены и как только данная цена будет установлена, вы получите сообщение от бота',
    )
