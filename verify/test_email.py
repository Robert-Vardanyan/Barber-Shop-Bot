import smtplib
import os
from email.mime.text import MIMEText
import random

# Podgruzka peremennix okrujeniya
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())


def send_email(user_mail, message):
    sender = os.getenv("EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg["Subject"] = "ПОДТВЕРЖДЕНИЕ УЧЕТНОЙ ЗАПИСИ"
        server.sendmail(sender, user_mail, msg.as_string())
        
        return f"The verify code was sent successfully in mail {user_mail}"
    
    except Exception as _ex:
        return f"{_ex}\nSomething wrong, check please!"


def verification(user_mail, user_name, code):
    message = f"Уважаемый(ая) {user_name},\n\nСпасибо за регистрацию в нашей системе. Для завершения процесса регистрации и подтверждения вашей учетной записи, вам необходимо выполнить следующее действие:\n\nПерейдите в Telegram и найдите нашего бота по имени @bs_exm_bot.\nВведите код подтверждения:\n\n\t{code}\n который предоставлен в сообщении от бота.\nЕсли у вас возникли какие-либо вопросы или затруднения, не стесняйтесь связаться с нашей службой поддержки.\n\nС уважением, Barber Shop Test"
    #print(send_email(user_mail, message=message))
    return send_email(user_mail, message=message)



