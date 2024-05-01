from aiogram import F, types, Router    #Ps. F --> magic filter
from aiogram.filters import CommandStart, Command, or_f , StateFilter #Ps. or_f --> kam commands-n a ashxatelu kam F_y (mek toxum grelu jamanak)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.formatting import as_list, as_marked_section, Bold #Ps. Formatavorac grelu hamar
# from aiogram.types import CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession
# Mnacac importner
from buttons import reply, inline
from datetime import date
from verify import  test_email as tm
import random

from database.data import df
from database import orm_query as orm

# EXCEL-i het ashxatelu hamar (PANDAS)
import pandas as pd

# User router-i stexcum (Ps. vor miacnenq Dispatcher-in main.py-um)
user_dp = Router()


#Registration

# Finite State Machine (FSM)(User reg)

class Registration(StatesGroup):
    # Steps of states
    user_id = State()
    reg_time = State()
    start_time = State()
    name = State()
    phone = State()
    mail = State()
    verify = State()

    texts = {
    'Registration:name': 'Մուտքագրեք Ձեր անունը կրկին.',
    'Registration:phone': 'Մուտքագրեք Ձեր հեռախոսահամարը կրկին.',
    'Registration:mail': 'Մուտքագրեք Ձեր mail կրկին.',
}

# Start cmd and (FSM reg)
@user_dp.message(CommandStart())
async def welcome(message: types.Message, state: FSMContext, session: AsyncSession):
    x_user = await orm.orm_check_user(session, message.from_user.id)
    if  str(type(x_user)) != "<class 'NoneType'>":
        user = await orm.orm_get_user(session, message.from_user.id)
        await message.answer(f"Բարի գալուստ {user.name} !", reply_markup=reply.start_but)
    else:
        # Fonayin tvyalneri havaqum
        await message.answer('Բարի Գալուստ BARBER BOT💇‍♂️', reply_markup=reply.del_kbd)
        now = (str(date.today())).split('-')
        await state.update_data(user_id=message.from_user.id)
        await state.set_state(Registration.reg_time)
        await state.update_data(reg_time=now)
        await state.set_state(Registration.start_time)
        await state.update_data(start_time=now)
        await state.set_state(Registration.start_time)
        await message.answer('Եկեք արագ լրացնենք Ձեր տվյալները...\nԻնչ է Ձեր անունը?')
        await state.set_state(Registration.name)

# Chexarkel
@user_dp.message(StateFilter('*'), Command("chexarkel"))
@user_dp.message(StateFilter('*'), F.text.casefold() == "chexarkel")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return
    
    await state.clear()
    await message.answer("Գործողությունը չեղարկված է")

# Veradarnal mek qayl het
@user_dp.message(StateFilter('*'), Command("het"))
@user_dp.message(StateFilter('*'), F.text.casefold() == "het")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state in Registration.__all_states__:
        if current_state == Registration.name:
            await message.answer('Նախորդ քայլ այլևս չկա , կամ մուտքագրեք անունը , կամ տվեք ՙՉեղարկել՚ հրամանը')
            return
        previous = None
        for step in Registration.__all_states__:
            if step.state == current_state:
                await state.set_state(previous)
                await message.answer(f"Լավ , դուք վերադարձաք նախորդ քայլին\n {Registration.texts[previous.state]}")
                return
            previous = step
    else:
        if current_state == Appointment.service:
            await message.answer('Նախորդ քայլ այլևս չկա , կամ մուտքագրեք անունը , կամ տվեք ՙՉեղարկել՚ հրամանը')
            return
        previous = None
        for step in Appointment.__all_states__:
            if step.state == current_state:
                await state.set_state(previous)
                await message.answer(f"Լավ , դուք վերադարձաք նախորդ քայլին\n {Appointment.texts[previous.state]}")
                return
            previous = step

# Petq e mshakel input arvox tvyalneri cshtutyuny
@user_dp.message(Registration.name, F.text)
async def reg(message: types.Message, state: FSMContext):
    if message.text.isalpha() and len(message.text) < 16 :
        await state.update_data(name=message.text)
        global user_name 
        user_name = message.text
        await message.answer('Գրեք Ձեր հեռախոսահամարը (374 12 34 56 78)')
        await state.set_state(Registration.phone)
    else:
        await message.answer('Ձեր մուտքագրած տվյալները սխալ են!')
@user_dp.message(Registration.name)
async def reg(message: types.Message, state: FSMContext):
    await message.answer('Ձեր մուտքագրած տվյալները սխալ ֆորմատի են!')

@user_dp.message(Registration.phone, F.text)
async def reg(message: types.Message, state: FSMContext):
    number = ''
    for i in message.text:
        if i.isdigit():
            number += i 
    if len(number) == 11:
        await message.answer(f'Ձեր հեռախոսահամարը +{number}')
        await state.update_data(phone=message.text)
        await message.answer('Գրեք Ձեր Email ...')
        await state.set_state(Registration.mail)
    else:
        await message.answer('Ձեր մուտքագրած տվյալները սխալ են!')
@user_dp.message(Registration.phone)
async def reg(message: types.Message, state: FSMContext):
    await message.answer('Ձեր մուտքագրած տվյալները սխալ ֆորմատի են!')

@user_dp.message(Registration.mail, F.text)
async def reg(message: types.Message, state: FSMContext):
    if '@' in message.text :
        char = '1234567890abcdefghijklmnopqrstuvwxyz'
        global code
        code = ''
        for i in range(6):
            x = random.choice(char)
            code += x
        print(tm.verification(message.text, user_name, code))
        await state.update_data(mail=message.text)
        await message.answer('Գրեք Ձեր Email եկած գաղտնաբառը...\nՀգ. Եթե նամակը չի գալիս , կխնդրեմ նայեք ՛Սպամ՛-ի մեջ, կամ ստուգեք մուտքագրված տվյալները:')
        await state.set_state(Registration.verify)
    else:
        await message.answer('Ձեր մուտքագրած տվյալները սխալ են!')
@user_dp.message(Registration.mail)
async def reg(message: types.Message, state: FSMContext):
    await message.answer('Ձեր մուտքագրած տվյալները սխալ ֆորմատի են!')
        
@user_dp.message(Registration.verify, F.text)
async def reg(message: types.Message, state: FSMContext, session: AsyncSession):
        if message.text == code:
            await state.update_data(verify='verify')
            user_info = await state.get_data()
            user_info['n_order'] = 0
            # await message.answer(str(user_info)) #Tpum e user-i tvylanery minchev basa uxarkely
            try:
                await orm.orm_add_user(session, user_info)
                print(f"🥳\tNew user register [id:{user_info['user_id']}]")
                await message.answer(f"✅ {user_info['name']} Ձեր տվյալները պահպանված են !", reply_markup=reply.start_but)
                await state.clear()

            except Exception as e:
                print(f" \tuser register base problem | cheack sql_client_base")
                await message.answer('arajacl e xndir client base-i het , xndrum em dimeq coder-in =(')
        else:
            await message.answer('Ձեր մուտքագրած տվյալները սխալ են!')
@user_dp.message(Registration.verify)
async def reg(message: types.Message, state: FSMContext):
    await message.answer('Ձեր մուտքագրած տվյալները սխալ ֆորմատի են!')
#-----------------------------------------

# FSM(order)
class Appointment(StatesGroup):
    service = State()
    day = State()
    hour = State()
    
    texts = {
    'Appointment:service': 'Ընտրեք ծառայությունը կրկին.',
    'Appointment:day': 'Ընտրեք օրը կրկին.',
}

# Reply buttons 

#Carayutyunnerin hasaneliutyun stanalu hamar
serv = pd.read_excel('./service/service.xlsx')

@user_dp.message(or_f(Command('grancum'), (F.text == '✅ Գրանցվել')))
async def appointment(message: types.Message, state: FSMContext, session: AsyncSession):
    delta = await orm.orm_check_order(session, message.from_user.id)
    if delta:
        b_service = {x : x for x in serv['service']}
        btns_service = inline.get_inlineMix_btns(btns=b_service,sizes=(1,))
        await message.answer('💇 Ընտրեք ծառայությունը', reply_markup=btns_service)
        await state.set_state(Appointment.service)
    else:
        await message.answer('Հարգելիս, Դուք այսօր արդեն գրանվել էք 😣')

@user_dp.callback_query(Appointment.service, F.data.in_({x for x in serv['service']}))
async def appointment(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(service=callback.data)
    data = pd.read_excel('./service/grafic.xlsx')
    b_day = {x : x for x in data.columns[1:] if data[x].isna().sum() != 0}
    btns_day = inline.get_inlineMix_btns(btns=b_day,sizes= (3,))
    await callback.message.answer('📆 Ընտրեք շաբաթվա օրը', reply_markup=btns_day)
    await state.set_state(Appointment.day)
@user_dp.message(Appointment.service)
async def reg(message: types.Message, state: FSMContext):
    await message.answer('Ձեր մուտքագրած տվյալները սխալ ֆորմատի են!')

@user_dp.callback_query(Appointment.day, F.data.in_(df.columns.tolist()))
async def appointment(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(day=callback.data)
    data = pd.read_excel('./service/grafic.xlsx')
    b_hour = {}
    for i, x in enumerate(data[callback.data]):
        if not isinstance(x, str):
            b_hour[data['Unnamed: 0'][i]] = data['Unnamed: 0'][i]
    btns_hour = inline.get_inlineMix_btns(btns=b_hour,sizes= (4,))
    await callback.message.answer(f'🕑 {callback.data} օրը, ժամը քանիսին՞', reply_markup=btns_hour)
    await state.set_state(Appointment.hour)
@user_dp.message(Appointment.day)
async def reg(message: types.Message, state: FSMContext):
    await message.answer('Ձեր մուտքագրած տվյալները սխալ ֆորմատի են!')

@user_dp.callback_query(Appointment.hour, F.data.in_(df.index.tolist()))
async def appointment(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.update_data(hour=callback.data)
    order = await state.get_data()
    order['user_id'] = callback.message.chat.id
    await state.clear()
    data = pd.read_excel('./service/grafic.xlsx')
    data.iat[int([x for x in data['Unnamed: 0']].index(order['hour'])),int(data.columns.tolist().index(order['day']))] = f"{order['service']}  |  {order['user_id']}"
    data.to_excel('./service/grafic.xlsx', index=False, index_label=False) 
    #await callback.message.answer(str(order))
    await callback.message.answer(f'Ձեր գրանցումը ստեղծված է\n\nԾառայությունը --> {order["service"]}\nՕրը     --> {order["day"]}\nԺամը    --> {order["hour"]}')
    
    await orm.orm_order(session, callback.message.chat.id)
@user_dp.message(Appointment.hour)
async def reg(message: types.Message, state: FSMContext):
    await message.answer('Ձեր մուտքագրած տվյալները սխալ ֆորմատի են!')

@user_dp.message(or_f(Command('jnjel'), (F.text == '💢 Ջնջել գրանցումը')))
async def granum_cmd(message: types.Message, session: AsyncSession):
    data = pd.read_excel('./service/grafic.xlsx')
    found = False
    for tiv, i in enumerate(data.columns[1:]):
        for index, j in enumerate(data[i]):
            if not  isinstance(j, float):
                if str(message.chat.id) in j:
                    data.iat[index, tiv+1] = ''
                    data.to_excel('./service/grafic.xlsx', index=False, index_label=False)  
                    await message.answer('Ձեր գրանցումը ջնջված է 🫥')
                    await orm.orm_delete_order(session, message.from_user.id)
                    found = True
                    break
        if found:
            break       
    else:
        await message.answer('Դուք դեռ չէք գրանցվել 🤨')


@user_dp.message(or_f(Command('vayr'), (F.text == '📍 Գտնվելու Վայրը')))
async def granum_cmd(message: types.Message):
    await message.answer('Մենք այստեղ ենք 📍')
    await message.answer_location(40.16982823565007, 44.51576421164086)

# @user_dp.message(or_f(Command('idram'), (F.text == '🧡 Իդրամ')))
# async def granum_cmd(message: types.Message):
#     await message.answer_photo(types.FSInputFile(path=r"./photo/idram.jpg"), caption="Sa el qez qr-y")

@user_dp.message(or_f(Command('soc'), (F.text == '🧡 Սոց. ցանց')))
async def granum_cmd(message: types.Message):
    cancer = {
        'Linkedin' : 'https://www.linkedin.com/in/robert-vardanyan-0753532b6/',
        'GitHub' : 'https://github.com/Robert-Vardanyan',
        'Facebook' :  'https://www.facebook.com/SmartCode.am/',
        'Instagram' : 'https://www.instagram.com/smartcode.am/',
        'Telegram' : 'https://t.me/rova_coder'
    }
    btns_cancer = inline.get_inlineMix_btns(btns=cancer,sizes= (2,))
    await message.answer('Ահա և մեր տվյալները 😉', reply_markup=btns_cancer)

@user_dp.message(or_f(Command('zang'), (F.text == '☎️ Զանգահարել')))
async def granum_cmd(message: types.Message):
    await message.answer_contact('+374 96 49 49 97','ROVA','Coder')
    
@user_dp.message(or_f(Command('gnacucak'), (F.text == '💰 Գնացուցակ')))
async def granum_cmd(message: types.Message):
    service = pd.read_excel('./service/service.xlsx')
    txt = ''
    for i in range(len(service.index)):
        txt += f'{service['service'][i]} = <u>{service['price'][i]}</u> ֏\n'
    await message.reply(txt)

#else
@user_dp.message()
async def granum_cmd(message: types.Message):
    await message.reply('🤷‍♂️ Ես Ձեզ չեմ հասկանում')