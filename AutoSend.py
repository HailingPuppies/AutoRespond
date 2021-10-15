from imap_tools import MailBox, A
import pandas as pd
import os


def auto_reply():
    with MailBox('imap.gmail.com').login('lifeupdate.msg@gmail.com', 'rvqeiqxcoftltxgg') as mailbox:
        item = [att[0].payload for att in [msg.attachments for msg in mailbox.fetch(A(seen=False), mark_seen=True)]]

    if len(item) == 0:
        return False



print(auto_reply())