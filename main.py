import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from emoji.core import emojize
from aiogram.utils.markdown import hbold, hcode, hlink

from gdz import GDZ
import db
from config import token, sql

logging.basicConfig(level=logging.DEBUG)
bot = Bot(token=token)
dp = Dispatcher(bot)


async def main_message(message: types.Message):
    await message.answer(db.gdz_help, parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                             KeyboardButton(emojize(
                                 f'Сжатие - {":cross_mark:" if sql.get_data(message.from_user.id, "upscaled") == 1 else ":check_mark_button:"}'))))


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    sql.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name,
                 message.from_user.last_name)
    await main_message(message)


@dp.message_handler(commands=['author'])
async def author(message: types.Message):
    await message.answer(f'Папа: {hlink("Алекса", "https://t.me/DWiPok")}'
                         f'\nИсходный код: {hlink("Github", "https://github.com/DarkWood312/gdz_bot_for_10b")}', parse_mode=types.ParseMode.HTML)


@dp.message_handler()
async def other_messages(message: types.Message):
    sql.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name,
                 message.from_user.last_name)
    low = message.text.lower()
    gdz = GDZ(message.from_user.id)

    if 'сжатие' in low:
        sql.change_data_int(message.from_user.id, 'upscaled',
                            False if sql.get_data(message.from_user.id, 'upscaled') == True else True)
        await message.answer(
            f'Отправка фотографий без сжатия {"включена" if sql.get_data(message.from_user.id, "upscaled") == True else "выключена"}!',
            reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(emojize(
                f'Сжатие - {":cross_mark:" if sql.get_data(message.from_user.id, "upscaled") == 1 else ":check_mark_button:"}'))))

    # *  gdz...
    elif ('алг' in low) or ('alg' in low):
        try:
            subject, num = low.split(' ', 1)
            num = int(num)
            response = await gdz.alg_euroki(num)
            for group in response:
                await message.answer_media_group(group)
        except ValueError:
            await message.answer('Некорректное число!')
        except ConnectionError:
            await message.answer('Не найдено заданием с таким номером!')

    elif ('гео' in low) or ('geo' in low):
        try:
            subject, num = low.split(' ', 1)
            num = int(num)
            response = await gdz.geom_megaresheba(num)
            for group in response:
                await message.answer_media_group(group)
        except ValueError:
            await message.answer('Некорректное число!')
        except ConnectionError:
            await message.answer('Не найдено заданием с таким номером!')

    elif ('анг' in low) or ('ang' in low):
        try:
            subject, page = low.split(' ', 1)
            page = int(page)
            response = await gdz.ang_euroki(page)
            for text in response:
                await message.answer(text)
            await message.answer(f'https://www.euroki.org/gdz/ru/angliyskiy/10_klass/vaulina-spotlight-693/str-{page}')
        except ValueError:
            await message.answer('Некорректное число!')
        except ConnectionError:
            await message.answer('Не найдено страницы с таким номером!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
