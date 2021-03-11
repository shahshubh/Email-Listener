import discord
import os
import email
import imaplib
from keep_alive import keep_alive
import random

colors = [0x00ff00, 0x000000]

async def filter_email(msg, message, bodyMsg):
  allEmails = ['shahshubh251@gmail.com', 'shahshubh009@gmail.com']
  for e in allEmails:
    if e in msg['From']:
      return True
  return False
  

async def listen_new_email(message):
  while 1:
    server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
    server.login(username, password)
    server.select('INBOX')
    result, data = server.search(None, 'UnSeen')

    uids = [int(s) for s in data[0].split()]
    for uid in uids:
      if uid > uid_max:
        result, data = server.fetch(str(uid), "(RFC822)")
        try:
          result = server.copy(str(uid),'Placement')
          await message.channel.send("Added your email to Placement Folder 😉\n")
        except Exception as error:
          print(error)
          print(error.args)
        for response in data:
          if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            if(msg.is_multipart()):
              payload = msg.get_payload()[0]
              bodyMsg = payload.get_payload()
            else:
              bodyMsg = msg.get_payload()

            
            # if(filter_email(msg, message, bodyMsg)):
            #   await message.channel.send(msg["Date"]+"\n"+msg["From"]+"\n"+msg["Subject"]+"\n"+bodyMsg)
            embedVar = discord.Embed(title="New Email", description=msg["From"], color=random.choice(colors))
            embedVar.add_field(name="Date", value=msg["Date"], inline=False)
            embedVar.add_field(name="Subject", value=msg["Subject"], inline=False)
            embedVar.add_field(name="Body", value=bodyMsg, inline=False)
            await message.channel.send(embed=embedVar)
            
            print(" ===============================")
            print(msg["Date"]+"\n"+msg["From"]+"\n"+msg["Subject"]+"\n"+bodyMsg)
            print("===============================\n")
    server.logout()


async def listen_email_handler(message):
  try:
    await listen_new_email(message)
  except:
    await message.channel.send("Some error occured !!")




client = discord.Client()

imap_ssl_host = 'imap.gmail.com'
imap_ssl_port = 993
username = os.getenv('EMAIL')
password = os.getenv('PASS')

uid_max = 0

server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
server.login(username, password)
server.select('INBOX')

result, data = server.search(None, 'UnSeen')

uids = [int(s) for s in data[0].split()]
if uids:
  uid_max = max(uids)
  # Initialize `uid_max`. Any UID less than or equal to `uid_max` will be ignored.

server.logout()



@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('!end'):
    await message.channel.send("Stopped listening to your emails !!")
    return
  if message.content.startswith('!start'):
    await message.channel.send("Listening to your emails...")
    await listen_email_handler(message)


keep_alive()
client.run(os.getenv('TOKEN'))





# EMAIL=shahshubh1010@gmail.com
# PASS=vmuvevtaflwipjkb
# import email_listener
# import os

# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# # Set your email, password, what folder you want to listen to, and where to save attachments
# email = os.getenv('EMAIL')
# app_password = os.getenv('PASS')
# folder = "Inbox"
# attachment_dir = ROOT_DIR + "/attachments"
# el = email_listener.EmailListener(email, app_password, folder, attachment_dir)

# # Log into the IMAP server
# el.login()

# # Get the emails currently unread in the inbox
# messages = el.scrape()
# print(messages)

# # Start listening to the inbox and timeout after an hour
# timeout = 60
# el.listen(timeout)