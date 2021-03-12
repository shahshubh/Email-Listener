import discord
import os
import imaplib
from keep_alive import keep_alive
from email_listener import email_listener

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

server.logout()


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  isAdmin = discord.utils.get(message.author.roles, name="ADMIN")
  if message.author == client.user:
    return
  if isAdmin is None:
    await message.channel.send("You are not admin")
    return
  else:
    if message.content.startswith('!end'):
      await message.channel.send("Stopped listening to your emails !!")
      return
    if message.content.startswith('!start'):
      await message.channel.send("Listening to your emails...")
      await email_listener(message, uid_max)


keep_alive()
client.run(os.getenv('TOKEN'))