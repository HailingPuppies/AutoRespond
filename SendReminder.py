import smtplib
from imap_tools import MailBox, A
import pandas as pd
import os
import time
from email.message import EmailMessage
from datetime import datetime
import parsedatetime as pdt

cal = pdt.Calendar()
now = datetime.now()

def send_reminder(content):
    msg = EmailMessage()

    msg['subject'] = ''
    msg['to'] = f'{sender}@vtext.com' # right now only works with verizon cuz of this
    msg['from'] = 'lifeupdate.msg@gmail.com'
    msg.set_content(response)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login('lifeupdate.msg@gmail.com',pswd)
    server.send_message(msg)
    server.quit()

for sender in os.listdir('users'):

    with open(f'users/{sender}/reminders.txt') as file:
        body = [w.split('@') for w in file.read().split('\n')]
        for reminder in body:
            if now > cal.parseDT(reminder[0])[0]:
                send_reminder(reminder[1])
        print(body)
