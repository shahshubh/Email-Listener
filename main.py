import discord
import os
import imaplib
from keep_alive import keep_alive
from email_listener import email_listener
import constants
import random

client = discord.Client()

imap_ssl_host = 'imap.gmail.com'
imap_ssl_port = 993

uid_max = 0

server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
server.login(constants.username, constants.password)
server.select('INBOX')

result, data = server.search(None, 'UnSeen')

uids = [int(s) for s in data[0].split()]
if uids:
  uid_max = max(uids)

server.logout()


def create_embed(title, description=""):
  embedVar = discord.Embed(title=title, description=description, color=random.choice(constants.colors))
  return embedVar

  
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  isAdmin = discord.utils.get(message.author.roles, name="ADMIN")
  # check if msg is sent by the bot
  if message.author == client.user or not message.content.startswith('!'):
    return

  # COMMON commands for all users 
  if message.content.startswith('!hello'):
    await message.channel.send("Hey "+message.author.name)
    return
  if message.content == '!list-whitelist':
    allEmailsString = ''
    for i in range(len(constants.whitelistEmails)):
      allEmailsString += str(i + 1) +". "+constants.whitelistEmails[i]+'\n'
    await message.channel.send(allEmailsString)
    return 
  if message.content == '!help':
    return


  # ADMIN commands
  if isAdmin is None:
    await message.channel.send("You are not admin")
    return

  else:
    if message.content.startswith('!clear'):
      number = int(message.content.split(' ')[1])
      deleted = await message.channel.purge(limit = number)
      embed = create_embed('Deleted {} message(s)'.format(len(deleted)))
      await message.channel.send(embed = embed)

    if message.content.startswith('!end'):
      await message.channel.send("Stopped listening to your emails !!")
      return

    if message.content.startswith('!start'):
      await message.channel.send("Listening to your emails...")
      await email_listener(message, uid_max)
      


keep_alive()
client.run(os.getenv('TOKEN'))