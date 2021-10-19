import smtplib
from imap_tools import MailBox, A
import pandas as pd
import os
import time
from email.message import EmailMessage
from datetime import datetime
import parsedatetime as pdt

SEND = True

def auto_reply():


    commands = ['add', 'clear', 'show','reminder', 'delete']
    user,pswd = 'lifeupdate.msg@gmail.com', 'rvqeiqxcoftltxgg'

    with MailBox('imap.gmail.com').login(user, pswd) as mailbox:
        try:
            texts = [att[0].payload.decode('utf-8') for att in [msg.attachments for msg in mailbox.fetch(A(seen=False), mark_seen=False)]]
        except:
            texts = [msg.text.replace("\r\n",'') for msg in mailbox.fetch(A(seen=False), mark_seen=False)]
        senders = [msg.from_ for msg in mailbox.fetch(A(seen=False), mark_seen=True)]
        #-------No New Messages will end the program-------
    if len(texts) == 0:
        return False

    print(texts)
    print(senders)
    # ----- now for the meat of it -------
    for message,sender in zip(texts,[s.split('@')[0] for s in senders]):
        exists = os.path.exists(f'users/{sender}')
        if not exists:
            # Create a new directory because it does not exist
            os.makedirs(f'users/{sender}')

        split_msg = message.split(' ')
        list_name,cmd = split_msg[0],(split_msg[1] if split_msg[1] in commands else None)
        content = ' '.join(split_msg[2:]) if len(split_msg) > 1 else ''
        print(list_name, '\n',cmd)
        # process and create message here



        response = globals()[cmd](sender,list_name,content)
        print('response: ',response)
        # send message
        if response is not None:
            SEND = True
        else:
            SEND = False

        if SEND:
            msg = EmailMessage()



            msg['subject'] = ''
            msg['to'] = f'{sender}@vtext.com' # right now only works with verizon cuz of this
            msg['from'] = user
            msg.set_content(response)
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(user,pswd)
            server.send_message(msg)
            server.quit()


    return True


def add(directory, list_name,content):
    with open(f'users/{directory}/{list_name.lower()}.txt','a+') as file:
        file.write(f'\n{content}')
        file.close()
    return show(directory,list_name)

def clear(directory,list_name,*args):
    with open(f'users/{directory}/{list_name.lower()}.txt', 'w+') as file:
        file.write('')
        file.close()
    return None

def delete(directory,list_name,*args):
    if os.path.exists(f'users/{directory}/{list_name.lower()}.txt'):
        os.remove(f'users/{directory}/{list_name.lower()}.txt')
    return None

def show(directory,list_name,*args):
    with open(f'users/{directory}/{list_name.lower()}.txt', 'r') as file:
        msg = file.read()
        file.close()
    return f'{list_name.upper()} LIST:{msg}'

def reminder(directory,command,phrase):
    cal = pdt.Calendar()
    now = datetime.now()
    dt = phrase.split(':')[0]
    to_remind = phrase.split(':')[1]
    with open(f'users/{directory}/reminders.txt','a+') as file:
        remind_time = cal.parseDT(dt, now)[0]

        if command == 'add':
            content = f'{to_remind} @ {remind_time}'
            file.write(f'\n{content}')

        if command == 'clear':
            file.truncate(0)

        if command == 'show':
            msg = file.read()
            return msg




auto_reply()