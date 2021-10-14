import datetime
import smtplib
import time
from email.message import EmailMessage
from email.mime import text as mtext
import email
import imaplib
import os
import PySimpleGUI as sg
import schedule


def send_text(body, to='3106130768@vtext.com', subject=None):

    msg = EmailMessage()
    msg.set_content(body)

    if subject is not None:
        msg['subject'] = subject

    msg['to'] = to

    user = 'lifeupdate.msg@gmail.com'
    password = "rvqeiqxcoftltxgg"  # App Password from Google

    msg['from'] = user

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()
    return body

send_text(f'words {time.ctime()}')