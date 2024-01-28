import random
from src.create_bot import _


class Messages:
    #  Статья с фото: https://telegra.ph/Foto-dlya-yuume-tg-bota-12-12

    @staticmethod
    def ask_for_locale() -> str:
        return (
            'Выберите язык ⤵️\n'
            'What is your language? ⤵'
        )

    @staticmethod
    def get_welcome(user_name: str = 'незнакомец') -> str:
        return _(
            "<b>Приветствую тебя, {user_name}!</b> \n\n"
            "<i>Что бы получить доступ к сигналам, <b>перейдите в канал по кнопке ниже и получите "
            "более подробную информацию 🔉</b></i> \n\n"
            "🔐 Если у вас есть кодовое слово для активации бота, то нажмите кнопку <b>«ПОЛУЧИТЬ СИГНАЛЫ»</b>"
        ).format(user_name=user_name)

    @staticmethod
    def get_welcome_photo() -> str:
        return 'https://telegra.ph/file/6f89ed9b10129ffc8c1be.png'

    @staticmethod
    def get_next_signal(onewin_id: int):
        coefficient = f'{random.uniform(1.30, 2.73):.2f}'
        return _('ID: {onewin_id} \n🚀 ВЫВОДИ НА: <b>{coefficient}</b>') \
            .format(onewin_id=onewin_id, coefficient=coefficient)

    @staticmethod
    def ask_for_code_word() -> str:
        return _('✍ Введите «кодовое слово», которое вам выдали:')

    @staticmethod
    def get_code_word_incorrect():
        return _('❗<b>Вы ввели неправильное кодовое слово!</b> \nПопробуйте ещё раз:')

    @staticmethod
    def ask_for_1win_id() -> str:
        return _('Замечательно! \nТеперь введите 🆔 от вашего аккаунта 1win: ')

    @staticmethod
    def get_1win_id_incorrect_length() -> str:
        return _('❗<b>ID не может содержать букв и символов, только цифры!</b> \nПопробуйте ещё раз:')

    @staticmethod
    def get_1win_id_have_forbidden_symbols() -> str:
        return _('❗<b>ID должно иметь длину в 8 цифр</b> \nПопробуйте снова:')

    @staticmethod
    def get_before_game_start() -> str:
        return _("Перед тем как, начать ⤵️\n\n" 
                 "Минимальная сумма депозита в игре с ботом <b>500-1000₽</b> либо <b>5-15$</b> \n\n" 
                 "Если вдруг бот выдает не верные коэффициенты, скорее всего ваш аккаунт <b>не активирован</b>. \n" 
                 "Нужно сделать депозит еще раз, чтобы ваш аккаунт активировался❗")

    @staticmethod
    def get_before_start_photo() -> str:
        return 'AgACAgIAAxkBAAEB_TtkzMl5s-HsM8JstC6FO4PRc4b6SAAC3cYxG5rOaErWm2hpoDD2pQEAAwIAA3kAAy8E'
