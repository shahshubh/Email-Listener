import discord
import imaplib
import email
import random
import constants

imap_ssl_host = 'imap.gmail.com'
imap_ssl_port = 993


def filter_email(msg):
  for e in constants.whitelistEmails:
    if e in msg['From']:
      return True
  return False
  

async def listen_new_email(message, uid_max):
  while 1:
    server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
    server.login(constants.username, constants.password)
    server.select('INBOX')
    result, data = server.search(None, 'UnSeen')

    uids = [int(s) for s in data[0].split()]
    for uid in uids:
      if uid > uid_max:
        result, data = server.fetch(str(uid), "(RFC822)")
        for response in data:
          if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            print("HERE")
            if(msg.is_multipart()):
              payload = msg.get_payload()[0]
              bodyMsg = payload.get_payload()
            else:
              bodyMsg = msg.get_payload()


        if(filter_email(msg)):
          try:
            result = server.copy(str(uid),'Placement')
            await message.channel.send("Added your email to Placement Folder 😉\n")
          except Exception as error:
            print(error)
          embedSubject = msg["Subject"] if msg["Subject"] != "" else "(No Subject)"
          embedBody = bodyMsg if bodyMsg != "" else "(No Body)"

          embedVar = discord.Embed(title="New Email", description=msg["From"], color=random.choice(constants.colors))
          embedVar.add_field(name="Date", value=msg["Date"], inline=False)
          embedVar.add_field(name="Subject", value=embedSubject, inline=False)
          embedVar.add_field(name="Body", value=embedBody, inline=False)
          await message.channel.send(embed=embedVar)
        
        print(" ===============================")
        print(msg["Date"]+"\n"+msg["From"]+"\n"+msg["Subject"]+"\n"+bodyMsg)
        print("===============================\n")
    server.logout()


async def email_listener(message, uid_max):
  try:
    await listen_new_email(message, uid_max)
  except:
    await message.channel.send("Some error occured !! Stopped listening to new email")