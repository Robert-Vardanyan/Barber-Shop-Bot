# Python standart moduls
import asyncio
import os

# Framework moduls
from aiogram import Bot , Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

# Podgruzka peremennix okrujeniya
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

# Mnacac importner
from handlers.user import user_dp  # User dp-i miacum Main-in
from commands.bot_cmd_list import user_private_cmd
import database.data as data

from middlewares.db import DataBaseSession
from database.engine import create_db, drop_db, session_maker
#...


# Bot and Parse_mode
bot = Bot(token = os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# Dispatchers
dp = Dispatcher()  #Ps. Main router
# Ayl router-neri miacum Dispatcher-in
dp.include_router(user_dp)  


# Bot START , STOP , and DATA create
async def on_startup(bot):
    os.system('cls')
    print('✅\tBot startup')
    df_param = True
    sql_drop = 0
    if df_param:
        df = data.df
        df.to_excel('./service/grafic.xlsx')
        print('✅\tCreated new Grafic (grafic.xlsx)')
    else:
        print('🟨\tUse old Grafic (grafic.xlsx)')
    
    if sql_drop:
        await drop_db()
        print('✂️\t Client base drop ...')
    await create_db()
    print('✅\tSuccessful client base interaction !')


    try:
        print('📂\tOpening service folder')
        print('👀\tSearch service file')
        x = open('./service/service.xlsx', 'r')
        print('✅\tFind service file\n')
    except:
        print('🛑\tDont find service file')
    finally:
        x.close

    print('✅ Bot worked successfully.\n')


async def on_shutdown(bot):
    print('✋\tBot shutdown')


#Blocked user 
# bot.restrict_chat_member(chat_id=,user_id=,can_send_messages=False)


#Ps. Boti ashxatanqi apahovum 
async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True) #Ps. chashxateluc --> ashxatel ancneluc hin chmshakvac sms-nery chen patasxanvum
    
    await bot.set_my_commands(commands=user_private_cmd, scope=types.BotCommandScopeAllPrivateChats()) # cmd list in User privat chat
    
    await dp.start_polling(bot)
asyncio.run(main())