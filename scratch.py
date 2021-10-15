import imaplib
from imap_tools import MailBox, A

with MailBox('imap.gmail.com').login('lifeupdate.msg@gmail.com', 'rvqeiqxcoftltxgg') as mailbox:
    item = [att[0].payload for att in [msg.attachments for msg in mailbox.fetch(A(seen=False), mark_seen=False)]]

print(len(item))