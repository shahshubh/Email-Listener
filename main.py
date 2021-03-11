# import discord
# import os
# import time
# from itertools import chain
# import email
# import imaplib
# import email_listener

# async def listen_new_email(message):
#   while 1:
#     server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
#     server.login(username, password)
#     server.select('INBOX')
#     result, data = server.search(None, 'UnSeen')

#     uids = [int(s) for s in data[0].split()]
#     for uid in uids:
#       if uid > uid_max:
#         result, data = server.fetch(str(uid), "(RFC822)")
#         for response in data:
#           if isinstance(response, tuple):
#             msg = email.message_from_bytes(response[1])
#             if(msg.is_multipart()):
#               payload = msg.get_payload()[0]
#               bodyMsg = payload.get_payload()
#             else:
#               bodyMsg = msg.get_payload()

#             await message.channel.send(msg["Date"]+"\n"+msg["From"]+"\n"+msg["Subject"]+"\n"+bodyMsg)
            
#             print(" ===============================")
#             print(msg["Date"]+"\n"+msg["From"]+"\n"+msg["Subject"]+"\n"+bodyMsg)
#             print("===============================\n")
#     server.logout()

# client = discord.Client()

# imap_ssl_host = 'imap.gmail.com'  # imap.mail.yahoo.com
# imap_ssl_port = 993
# username = os.getenv('EMAIL')
# password = os.getenv('PASS')

# uid_max = 0

# server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
# server.login(username, password)
# server.select('INBOX')

# result, data = server.search(None, 'UnSeen')

# uids = [int(s) for s in data[0].split()]
# if uids:
#     uid_max = max(uids)
#     # Initialize `uid_max`. Any UID less than or equal to `uid_max` will be ignored subsequently.

# server.logout()



# @client.event
# async def on_ready():
#   print('We have logged in as {0.user}'.format(client))


# @client.event
# async def on_message(message):
#   if message.author == client.user:
#     return
#   if message.content.startswith('!end'):
#     await message.channel.send("Stopped listening to your emails !!")
#     return
#   elif message.content.startswith('!start'):
#     await message.channel.send("Listening to your emails...")
#     await listen_new_email(message)


# client.run(os.getenv('TOKEN'))


import email_listener
import os

# Set your email, password, what folder you want to listen to, and where to save attachments
email = os.getenv('EMAIL')
app_password = os.getenv('PASS')
folder = "Inbox"
# attachment_dir = "/path/to/attachments"
el = email_listener.EmailListener(email, app_password, folder)

# Log into the IMAP server
el.login()

# Get the emails currently unread in the inbox
messages = el.scrape()
print(messages)

# Start listening to the inbox and timeout after an hour
timeout = 60
el.listen(timeout)