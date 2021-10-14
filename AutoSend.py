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

def get_message(user='lifeupdate.msg@gmail.com', password='rvqeiqxcoftltxgg', most_recent_uid=None):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(user, password)
    mail.select('inbox')
    result, data = mail.uid('search', 'ALL')
    inbox_item_list = data[0].split()
    most_recent = inbox_item_list[-1]
    print('Most Recent UID = ')
    print(most_recent.decode('utf-8'),most_recent_uid)
    print(most_recent_uid != most_recent.decode('utf-8'))
    if most_recent_uid != most_recent.decode('utf-8'):

        result2, email_data = mail.uid('fetch', most_recent, '(RFC822)')
        raw_data = email_data[0][1].decode('utf-8')
        actual_message = email.message_from_string(raw_data)

        # downloading attachments
        for part in actual_message.walk():
            # this part comes from the snipped I don't understand yet...
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            file_name = part.get_filename()

            if bool(file_name): #this will overwrite the most recent text, if that matters, this is where to change it
                file_path = os.path.join('downloaded_messages/', file_name)

                fp = open(file_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()

                # subject = str(actual_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
                print('Downloaded "{file}" from email titled ____ with UID {uid}.'.format(file=file_name,uid=most_recent.decode('utf-8')))
                print(f'Downloaded {file_path}')
                read_and_reply(file_path)
                return most_recent.decode('utf-8')
            else:
                print('Something is weird:',file_name)

    elif most_recent_uid == most_recent.decode('utf-8'):
        # print('Already read')
        return most_recent.decode('utf-8')
    else:
        print('How did we get here??')
    # print(actual_message['From'],actual_message['To'],actual_message.get_content_type(),actual_message.get_payload())

def get_most_recent_uid(user='lifeupdate.msg@gmail.com', password='rvqeiqxcoftltxgg'):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(user, password)
    mail.select('inbox')
    result, data = mail.uid('search', 'ALL')
    inbox_item_list = data[0].split()
    return inbox_item_list[-1].decode('utf-8')



def read_and_reply(file_path):
    with open(file_path) as f:
        message = f.read()

    # here will go all of the different ways I'll respond to myself

    if message == 'Rules':
        sent = send_text('Here are some rules:\n1.\n2.')
        follow_up = send_text('Would you like to reply?\nhttps://mail.google.com/mail/u/5/#inbox' )
        # print(f'Sending text!\n{follow_up}')

    else:
        sent = send_text(message)
        # print(f'Sending text!\n{sent}')







if __name__ == '__main__':
    recent_uid = get_most_recent_uid()
    print('a',recent_uid)
    recent_uid = get_message(most_recent_uid=40)
    print('b',recent_uid)
    send_text(f'words {time.ctime()}')