import smtplib
from imap_tools import MailBox, A
import pandas as pd
import os
import time
from email.message import EmailMessage

SEND = False

def auto_reply():

    commands = ['Email', 'Text', 'Calendar', 'Research', 'Reminder']
    commands2 = ['add', 'clear', 'list']
    user,pswd = 'lifeupdate.msg@gmail.com', 'rvqeiqxcoftltxgg'

    with MailBox('imap.gmail.com').login(user, pswd) as mailbox:
        texts = [att[0].payload for att in [msg.attachments for msg in mailbox.fetch(A(seen=False), mark_seen=False)]]
        senders = [msg.from_ for msg in mailbox.fetch(A(seen=False), mark_seen=False)]
        #-------No New Messages will end the program-------
    if len(texts) == 0:
        return False



    # ----- now for the meat of it -------
    for message,sender in zip([t.decode('utf-8') for t in texts],[s.split('@')[0] for s in senders]):

        exists = os.path.exists(f'{sender}')
        if not exists:
            # Create a new directory because it does not exist
            os.makedirs(f'{sender}')

        split_msg = message.split(' ')
        cmd,cmd2 = split_msg[0],(split_msg[1] if split_msg[1] in commands2 else None)
        content = ' '.join(split_msg[1:]) if len(split_msg) > 1 else ''
        print(cmd, '\n',cmd2)
        # process and create message here
        add(sender,'Email','email this person')
        clear(sender,'Email')
        response = f'sent {time.ctime()}'
        # send message
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
    with open(f'{directory}/{list_name.lower()}.txt','a+') as file:
        file.write(f'\n{content}')
        file.close()

def clear(directory,list_name):
    with open(f'{directory}/{list_name.lower()}.txt', 'w+') as file:
        file.write('')
        file.close()




print(auto_reply())