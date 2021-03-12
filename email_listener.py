import discord
import imaplib
import os
import email
import random

colors = [0x00ff00, 0x000000]
allEmails = ['shahshubh251@gmail.com', 'shahshubh009@gmail.com']

imap_ssl_host = 'imap.gmail.com'
imap_ssl_port = 993
username = os.getenv('EMAIL')
password = os.getenv('PASS')

async def filter_email(msg, message, bodyMsg):
  for e in allEmails:
    if e in msg['From']:
      return True
  return False
  

async def listen_new_email(message, uid_max):
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


async def email_listener(message, uid_max):
  try:
    await listen_new_email(message, uid_max)
  except:
    await message.channel.send("Some error occured !!")