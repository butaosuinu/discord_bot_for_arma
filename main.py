import discord
import urllib.request
import re
import os
from os.path import join, dirname
from dotenv import load_dotenv

from pyquery import PyQuery as pq

dotenvPath = join(dirname(__file__), '.env')
load_dotenv(dotenvPath)

token = os.environ.get('TOKEN')

client = discord.Client()

def getDiffMcc(msg):
  oldAddons = []
  newAddons = []
  if msg.attachments.filename.startswith('MCC'):
    print(msg.attachments.filename)
    fileUrl = msg.attachments.url
    res = urllib.request.urlopen(filename).read()
    doc = pq(res)

if __name__ == '__main__':
  @client.event
  async def on_message(msg):
    pattern = re.compile(r"^(それな|せやな|セヤナ|ｾﾔﾅ|seyana|sorena)")
    if pattern.search(msg.content):
      if client.user != msg.author:
        m = 'わかる'
        await client.send_message(msg.channel, m)

    if re.search(r"クソゲー|くそげー", msg.content) and client.user != msg.author:
      m = 'やめたら？このゲーム'
      await client.send_message(msg.channel, m)

    if msg.content.startswith('どうかな') and client.user != msg.author:
      with open('img/wakaru.jpg', 'rb') as f:
        await client.send_file(msg.channel, f)

    if re.search(r"DJRN|だじ|ダジ|ﾀﾞｼﾞ", msg.content) and client.user != msg.author:
      m = '汚いからやめて'
      await client.send_message(msg.channel, m)

    if re.search(r"^(六|6)番ちゃんかわいい", msg.content) and client.user != msg.author:
      m = 'えへへ…'
      await client.send_message(msg.channel, m)

  client.run(token)