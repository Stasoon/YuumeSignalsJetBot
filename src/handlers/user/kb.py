from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData

from src.create_bot import _


class Keyboards:
    locale_callback_data = CallbackData('locale', 'language_code')

    @staticmethod
    def get_locale() -> InlineKeyboardMarkup:
        russian_button = InlineKeyboardButton(
            text='Русский 🇷🇺', callback_data=Keyboards.locale_callback_data.new(language_code='ru'))
        english_button = InlineKeyboardButton(
            text='English 🇬🇧', callback_data=Keyboards.locale_callback_data.new(language_code='en'))

        return InlineKeyboardMarkup(row_width=1).add(russian_button, english_button)

    @staticmethod
    def get_welcome_menu() -> InlineKeyboardMarkup:
        channel_url = 'https://t.me/+3EOCy8d0KRE3NDYy'
        channel_button = InlineKeyboardButton(text=_('🚨 ПОДПИСАТЬСЯ НА КАНАЛ 🚨'), url=channel_url)
        start_button = InlineKeyboardButton(text=_('🤖 ПОЛУЧИТЬ СИГНАЛЫ 🤖'), callback_data='welcome_menu')
        return InlineKeyboardMarkup(row_width=1).add(channel_button, start_button)

    @staticmethod
    def get_first_signal_markup() -> InlineKeyboardMarkup:
        first_signal = InlineKeyboardButton(_('▶ ПОЛУЧИТЬ СИГНАЛ ▶'), callback_data='next_signal')
        return InlineKeyboardMarkup(row_width=2).add(first_signal)

    @staticmethod
    def get_next_signal_markup() -> InlineKeyboardMarkup:
        next_signal = InlineKeyboardButton(_('СЛЕДУЮЩИЙ РАУНД ➡'), callback_data='next_signal')
        return InlineKeyboardMarkup(row_width=2).add(next_signal)

