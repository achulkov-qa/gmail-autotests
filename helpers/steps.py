from __future__ import print_function

import base64
import mimetypes
import os
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from googleapiclient.errors import HttpError
import allure
from common.journal import sender, to, subject, message_text, message_text_with_attachment, file_dir
from test.conftest import l_error


@allure.step('Создание письма')
def create_message(message_text=message_text, sender=sender, to=to, subject=subject):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

@allure.step('Создание черновика')
def create_draft(service, message_body, user_id='me'):
    try:
        message = {'message': message_body}
        draft = service.users().drafts().create(userId=user_id, body=message).execute()
        return draft
    except HttpError as error:
        l_error('Произошла ошибка: %s' % error)

@allure.step('Создание письма с вложением')
def create_message_with_attachment(filename, message_text=message_text_with_attachment, file_dir=file_dir,
                                   sender=sender, to=to, subject=subject):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    path = os.path.join(file_dir, filename)
    content_type, encoding = mimetypes.guess_type(path)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(path, 'rb')
        msg = MIMEApplication(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(path, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(path, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(path, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()

    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

@allure.step('Отправка письма')
def send_message(service, message, user_id='me'):
    try:
        result = (service.users().messages().send(userId=user_id, body=message).execute())
        return result
    except HttpError as error:
        l_error('Произошла ошибка: %s' % error)

@allure.step('Отправка письма-черновика')
def send_draft_message(service, draft, user_id='me'):
    try:
        result = (service.users().drafts().send(userId=user_id, body=draft).execute())
        return result
    except HttpError as error:
        l_error('Произошла ошибка: %s' % error)