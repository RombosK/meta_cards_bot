import os
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import callback_query
from aiogram.utils import executor
from aiogram import types

from config import Config, load_config

config: Config = load_config()
PHOTO_FOLDER = 'photos'
for admin_id in config.tg_bot.admin_ids:
    ADMIN_ID = admin_id
bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
dp: Dispatcher = Dispatcher(bot)

photo_files = os.listdir(PHOTO_FOLDER)

random.shuffle(photo_files)  # Перемешиваем файлы, чтобы выбирать случайные фото
random.choice(photo_files)


# def create_keyboard():
#     keyboard = types.InlineKeyboardMarkup()
#     for i in range(100):  # Создаем 100 кнопок
#         button = types.InlineKeyboardButton(text=f"Button {i + 1}", callback_data=f"button_{i + 1}")
#         keyboard.add(button)
#     return keyboard

# import glob
# from PIL import Image


@dp.message_handler(commands=['start', 'restart'])
async def cmd_start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton(text='Задать вопрос 🎲', callback_data='get_photo')
    button_2 = types.InlineKeyboardButton(text='Перезапустить бота ⏳', callback_data='restart_bot')
    keyboard.add(button_1)
    keyboard.add(button_2)
    await message.answer("Метафорические карты — это инструмент для работы с сознанием и подсознанием, который "
                         "используется в психологии, коучинге, терапии и других областях. Это набор карточек, на каждой"
                         " из которых изображена метафора, символ, иллюстрация или текст, который помогает "
                         "визуализировать определенную ситуацию, проблему или цель.Они помогают уловить тонкости и"
                         " нюансы неосознаваемых проблем, учитывая индивидуальный опыт, личные ассоциации и традиции,"
                         " и могут стать мощным инструментом для переосмысления, поиска новых решений и достижения "
                         "личных целей.\n\n"
                         "Сконцентрируйтесь над своим вопросом,чётко сформулируйте его одним предложением, затем "
                         "вытяните карту.\n\n"
                         "Чтобы сбросить каскад перезагрузите бота кнопкой. \n\n"
                         "Оригинальная идея Алины Малиновской на сайте www.metacards.fun",
                         reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'get_photo')
async def process_callback_get_photo(callback_query: types.CallbackQuery):
    photo_file = photo_files.pop(0)
    with open(os.path.join(PHOTO_FOLDER, photo_file), 'rb') as photo:
        # img = random.choice(glob.glob('photos/*.jpg'))
        # jpg = Image.open(img, + 'r')

        keyboard = types.InlineKeyboardMarkup()
        button_more_photo = types.InlineKeyboardButton(text='Следующий вопрос 🎲', callback_data='more_photo')
        button_2 = types.InlineKeyboardButton(text='Перезапустить бота ⏳', callback_data='restart_bot')
        keyboard.add(button_more_photo)
        keyboard.add(button_2)
        await bot.send_photo(callback_query.from_user.id, photo, reply_markup=keyboard)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == 'more_photo')
async def process_callback_more_photo(callback_query: types.CallbackQuery):
    photo_file = photo_files.pop(0)  # Take the next file from the list
    with open(os.path.join(PHOTO_FOLDER, photo_file), 'rb') as photo:
        keyboard = types.InlineKeyboardMarkup()
        button_more_photo = types.InlineKeyboardButton(text='Следующий вопрос 🎲', callback_data='more_photo')
        button_2 = types.InlineKeyboardButton(text='Перезапустить бота ⏳', callback_data='restart_bot')
        keyboard.add(button_more_photo)
        keyboard.add(button_2)
        await bot.send_photo(callback_query.from_user.id, photo, reply_markup=keyboard)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == 'restart_bot')
async def process_callback_restart_bot(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, "Бот будет перезапущен ⚛", show_alert=True)
    await bot.send_message(callback_query.from_user.id, "Бот перезапущен. Нажмите /start для начала работы ⚛")


@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, commands=['admin'])
async def cmd_admin(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton(text='Добавить карту 🪄', callback_data='add_photo')
    # button_2 = types.InlineKeyboardButton(text='Удалить фото', callback_data='remove_photo')
    keyboard.add(button_1)
    # keyboard.add(button_2)
    await message.reply("Меню администратора ⚡⚡⚡", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'add_photo')
async def process_callback_add_photo(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Отправьте мне карту, которую вы хотите добавить")


@dp.message_handler(lambda message: message.from_user.id == ADMIN_ID, content_types=['photo'])
async def handle_docs_photo(message):
    file_info = await bot.get_file(message.photo[-1].file_id)
    if file_info.file_path:
        file_name = file_info.file_path.split('/')[-1]
        await bot.download_file(file_info.file_path, destination=os.path.join(PHOTO_FOLDER, file_name))
        await message.reply("Карта добавлена")
    else:
        await message.reply("Ошибка при загрузке карты")


# @dp.callback_query_handler(lambda c: c.data == 'remove_photo')
# async def process_callback_remove_photo(callback_query: types.CallbackQuery):
#     keyboard = create_keyboard()
#     # keyboard = types.InlineKeyboardMarkup()
#     for photo in photo_files:
#         button = types.InlineKeyboardButton(text=photo, callback_data=f'remove_{photo}')
#         keyboard.add(button)
#     await bot.send_message(callback_query.from_user.id, "Выберите фото для удаления", reply_markup=keyboard)
#
#
# @dp.callback_query_handler(lambda c: c.data.startswith('remove_'))
# async def process_callback_remove_photo_confirm(callback_query: types.CallbackQuery):
#     photo_file = callback_query.data.split('_')[1]
#     os.remove(os.path.join(PHOTO_FOLDER, photo_file))
#     photo_files.remove(photo_file)
#     await bot.answer_callback_query(callback_query.id, "Фото удалено", show_alert=True)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

