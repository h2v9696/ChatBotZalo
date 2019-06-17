# encoding=utf8
import sys
from rivescript import RiveScript
import re

bot2 = RiveScript(utf8=True)
bot2.load_directory("eg/brain")
bot2.unicode_punctuation = re.compile(r'[.,!?;:]')
bot2.sort_replies()

while True:
    msg = raw_input('You> ')
    if msg == '/quit':
        quit()

    reply = bot2.reply("teabot", msg)
    print 'Bot>', reply
