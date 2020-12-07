import socks
import socket
from simplegmail import Gmail
import re

# 科学上网，你也需要科学使用代理，不然科学不了外网，也许你不会需要。
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Connection': 'close'
}
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1")
socket.socket = socks.socksocket

gmail = Gmail()

# Unread messages in your inbox
messages = gmail.get_unread_messages(include_spam_trash=True)

# messages = gmail.get_spam_messages()

# ...and many more easy to use functions can be found in gmail.py!

# Print them out!
for message in messages:
    if message.attachments:
        for attm in message.attachments:
            print('File: ' + attm.filename)
            matches = re.match(r'(\d{2})[_-](\d+)[_-](.+).ipynb', attm.filename)
            if matches:
                attm.save(filepath=f'{matches.group(1)}/作业/{matches.group(1)}_{matches.group(2)}.ipynb', overwrite=False)
                message.mark_as_read()
