import os

username = os.getenv('EMAIL')
password = os.getenv('PASS')
allEmails = ['shahshubh251@gmail.com', 'shahshubh009@gmail.com']
colors = [0x00ff00, 0x413c69, 0x4a47a3, 0x709fb0, 0x93329e, 0xf48b29]
commands = {
  '!hello': 'Greetings',
  '!list-whitelist': 'List of all whitelisted emails',
  '!clear': '!clear x Delete last x messages. where x is any number',
  '': '',
}