import asyncio
import os.path
import random

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from src.create_bot import i18n
from src.database import users, admin
from src.utils import send_typing_action, throttle
from src.misc import UserDataInputting
from .messages import Messages
from .kb import Keyboards
from config import CODE_WORD, Config


admin_photo_ids = {}


def get_admin_image_file_id(admin_id: int) -> str | None:
    photos_txt_filename = 'video_images.txt'

    if not os.path.exists(photos_txt_filename):
        return None

    with open(photos_txt_filename) as file:
        lines = file.readlines()
        index = admin_photo_ids.get(admin_id, 0)

        if index >= len(lines):
            index = 0

        image_file_id = lines[index].strip()
        admin_photo_ids[admin_id] = (index + 1) % len(lines)

    return image_file_id


def get_random_user_photo():
    images = [
        'AgACAgIAAxkBAAMJZXoTm4bGTzDk3XmGJyn91xQ9ESsAAorXMRs7DNFLiWO-Uwv8kyYBAAMCAANzAAMzBA',
        'AgACAgIAAxkBAAMKZXoTm0qrdN_EksTHj3Rum3bgBkkAAovXMRs7DNFLudep-3L0xxgBAAMCAANzAAMzBA',
        'AgACAgIAAxkBAAMLZXoTm-tFDkqnZZgiGVkX2B1_0iAAAozXMRs7DNFL02ydwBm8NNwBAAMCAANzAAMzBA',
        'AgACAgIAAxkBAAMMZXoTm5cmX3X5KlgAARfT1d1MSk4OAAKN1zEbOwzRS1gqBnxHhYorAQADAgADcwADMwQ',
        'AgACAgIAAxkBAAMNZXoTm5e2nhUMkXHp2ngmAdRtDUIAAo7XMRs7DNFLa5-aTUVi5WkBAAMCAANzAAMzBA',
        'AgACAgIAAxkBAAMOZXoTm-sbh1ZxUGMFDblarTnlVNAAAo_XMRs7DNFLXB5xGPVuePoBAAMCAANzAAMzBA',
        'AgACAgIAAxkBAAMPZXoTmxrlfHhyAieIX8GOlXKxrzYAApDXMRs7DNFLSatA0zbFk7oBAAMCAANzAAMzBA',
        'AgACAgIAAxkBAAMQZXoTm3pY65AppubYtv1ty_JIV_0AApHXMRs7DNFLNvkySdlA-7MBAAMCAANzAAMzBA',
        'AgACAgIAAxkBAAMRZXoTm70yT5gIGUeLEy5CZon36bYAApLXMRs7DNFLolyQM9Jc2OABAAMCAANzAAMzBA',
        'AgACAgIAAxkBAAMSZXoTm-5VzAd6tppU-1ME_dDratIAApPXMRs7DNFL4SpWiYphKtMBAAMCAANzAAMzBA',
        'AgACAgIAAxkBAAMTZXoTm00x8XhhorxuBnKnTrYQQWgAApTXMRs7DNFLBHTW-gP_HOcBAAMCAANzAAMzBA',
        'AgACAgIAAxkBAAMUZXoTm0Tw-LlhGqvwYSLfijLNjT4AApXXMRs7DNFLhuRoMP6-vJkBAAMCAANzAAMzBA',
        'AgACAgIAAxkBAAMVZXoTmzHGaSE7qXtP_oqcl4EIQaEAApbXMRs7DNFLBeM-LUCWwVoBAAMCAANzAAMzBA',
        'AgACAgIAAxkBAAMWZXoTmzV9UWpc_Dn3pHCuvZId5oEAApfXMRs7DNFLbPxsyXUMpwEBAAMCAANzAAMzBA',
    ]
    return random.choice(images)


async def edit_to_new_signal(to_message: Message, img_file_id: str):
    msg = await to_message.answer('⏳')
    delay_seconds = 0.8
    await asyncio.sleep(delay_seconds)

    await msg.delete()
    await msg.answer_photo(photo=img_file_id, reply_markup=Keyboards.get_next_signal_markup())


# region Handlers

@throttle()
async def __handle_start_command(message: Message, state: FSMContext) -> None:
    await state.finish()
    await send_typing_action(message)

    users.create_or_update_user(
        telegram_id=message.from_id,
        name=message.from_user.username or message.from_user.full_name,
        reflink=message.get_full_command()[1]
    )

    await message.answer(text=Messages.ask_for_locale(), reply_markup=Keyboards.get_locale())


async def __handle_locale_callback(callback: CallbackQuery, callback_data: Keyboards.locale_callback_data):
    await send_typing_action(callback.message)
    await callback.message.delete()

    language_code = callback_data.get('language_code')
    users.set_locale(callback.from_user.id, language_code)
    i18n.set_locale(new_lang_code=language_code)

    await callback.message.answer_photo(
        photo=Messages.get_welcome_photo(),
        caption=Messages.get_welcome(callback.from_user.first_name),
        reply_markup=Keyboards.get_welcome_menu(),
    )


@throttle(rate=1)
async def __handle_start_callback(callback: CallbackQuery, state: FSMContext):
    await send_typing_action(callback.message)
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    user_onewin_id = users.get_user_1win_id(telegram_id=callback.from_user.id)

    if not user_onewin_id:
        await callback.message.answer(Messages.ask_for_code_word())
        await state.set_state(UserDataInputting.wait_for_password.state)
    else:
        await callback.message.answer(
            text=Messages.get_before_game_start(),
            reply_markup=Keyboards.get_first_signal_markup()
        )


async def __handle_user_password_message(message: Message, state: FSMContext):
    await send_typing_action(message)

    if message.text.lower() == CODE_WORD.lower():
        await message.answer(text=Messages.get_before_game_start(), reply_markup=Keyboards.get_first_signal_markup())
        users.set_user_1win_id(telegram_id=message.from_user.id, onewin_id=1)
        await state.finish()
        # await message.answer(Messages.ask_for_1win_id())
        # await state.set_state(await UserDataInputting.next())
    else:
        await message.answer(Messages.get_code_word_incorrect())


# async def __handle_user_id_message(message: Message, state: FSMContext):
#     await send_typing_action(message)
#
#     if not message.text.isdigit():
#         await message.answer(Messages.get_1win_id_incorrect_length())
#         return
#     if len(message.text) != 8:
#         await message.answer(Messages.get_1win_id_have_forbidden_symbols())
#         return
#
#     users.set_user_1win_id(message.from_user.id, message.text)
#     await message.answer(text=Messages.get_before_game_start(), reply_markup=Keyboards.get_first_signal_markup())
#     await state.finish()


async def __handle_next_signal_callback(callback: CallbackQuery):
    await send_typing_action(callback.message)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()

    admin_ids = [*admin.get_admin_ids(), *Config.ADMIN_IDS]
    file_id = (
        get_random_user_photo()
        if callback.from_user.id not in admin_ids
        else get_admin_image_file_id(admin_id=callback.from_user.id)
    )

    if callback.from_user.id in admin_ids and not file_id:
        await callback.message.answer('Фото не добавлены!')
        return

    await edit_to_new_signal(to_message=callback.message, img_file_id=file_id)


# endregion
async def print_file_id(message):
    print(message.photo[0].file_id)


def register_user_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(print_file_id, content_types=['photo'])

    # обработка команды /start
    dp.register_message_handler(__handle_start_command, commands=['start'], state='*')

    # выбор языка
    dp.register_callback_query_handler(__handle_locale_callback, Keyboards.locale_callback_data.filter())

    # обработка кнопок приветственного меню
    dp.register_callback_query_handler(__handle_start_callback, text='welcome_menu', state=None)
    # dp.register_message_handler(__handle_user_id_message, state=UserDataInputting.wait_for_id)
    dp.register_message_handler(__handle_user_password_message, state=UserDataInputting.wait_for_password)

    # обработка нажатия на Следующий сигнал
    dp.register_callback_query_handler(__handle_next_signal_callback, text='next_signal')
