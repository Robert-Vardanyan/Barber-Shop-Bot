# Variant 1
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
# Variant 2
from aiogram.utils.keyboard import ReplyKeyboardBuilder


start_but = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='✅ Գրանցվել'),
            KeyboardButton(text='💢 Ջնջել գրանցումը'),

        ],
        [
            KeyboardButton(text='☎️ Զանգահարել'),
            KeyboardButton(text='📍 Գտնվելու Վայրը'),
        ],
        [
            KeyboardButton(text='🧡 Սոց. ցանց'),
            KeyboardButton(text='💰 Գնացուցակ'),
        ]
    ],
    resize_keyboard=True, #Ps. vor gracin hamapatasxan ereva
    input_field_placeholder='Հն սրտիկդ ինչ կուզի 🤔'
)

del_kbd = ReplyKeyboardRemove()


# Funkcia vor texum miangamic stexcenq knopkaner (tesaneli e darcnum handlerum ogtagorceluc)
def get_keyboard(
    *btns: str,
    placeholder: str = None,
    request_contact: int = None,
    request_location: int = None,
    sizes: tuple[int] = (2,),
):
    '''
    Parameters request_contact and request_location must be as indexes of btns args for buttons you need.
    Example:
    get_keyboard(
            "Меню",
            "О магазине",
            "Варианты оплаты",
            "Варианты доставки",
            "Отправить номер телефона",
            placeholder="Что вас интересует?",
            request_contact=4,
            sizes=(2, 2, 1)
        )
    '''
    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):
        
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))

        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
            resize_keyboard=True, input_field_placeholder=placeholder)