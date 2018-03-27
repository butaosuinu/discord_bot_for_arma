import discord
import urllib.request
import re
import os
from os.path import join, dirname
from dotenv import load_dotenv

from pyquery import PyQuery as pq

headers = { "User-Agent" :  "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)" }

dotenvPath = join(dirname(__file__), '.env')
load_dotenv(dotenvPath)

token = os.environ.get('TOKEN')

client = discord.Client()


def getAddonListToPreset(url):
  req = urllib.request.Request(url, None, headers)
  res = urllib.request.urlopen(req).read()
  doc = pq(res)
  doc = doc('td').items()
  addonList = list(filter(lambda i: i.attr('data-type') == 'DisplayName', doc))
  addonList = [i.text() for i in addonList]

  return addonList

def diffPreset(originalFileUrl, newFileUrl):
  oldAddons = getAddonListToPreset(originalFileUrl)
  newAddons = getAddonListToPreset(newFileUrl)

  diffAdd = list(set(newAddons) - set(oldAddons))
  diffDel = list(set(oldAddons) - set(newAddons))
  diffAdd.sort()
  diffDel.sort()

  print(diffAdd)
  print(diffDel)

  dist = '新しく追加したaddonはこれだよ！\n'
  for d in diffAdd:
    dist += d + '\n'

  dist += '\n'
  dist += '削除したaddonはこれ！\n'
  for d in diffDel:
    dist += d + '\n'

  return dist

def viewPreset(url):
  addonList = getAddonListToPreset(url)
  addonList.sort()
  dist = 'プリセット内容：\n'
  for addon in addonList:
    dist += addon + '\n'

  return dist

def viewHelp():
  text = 'コマンド説明\n'
  text += '--------------------------------\n'
  text += '!diff_preset : プリセットファイルをアップロードする時にコメントにこのコマンドを入力するとプリセットの差分が見れるよ！\n'
  text += '私のアナウンスに沿って差分を取りたい対象のプリセットファイルをアップロードしてね\n'
  text += '!view_preset : プリセットの内容が見れるよ\n'
  text += 'プリセットファイルアップ時にコメントにこのコマンドを書き込むか、アナウンスに沿ってプリセットファイルをアップロードしてね\n'
  text += '!help : この説明が見れるよ！\n'
  return text

if __name__ == '__main__':
  @client.event
  async def on_message(msg):
    pattern = re.compile(r"^(それな|せやな|セヤナ|ｾﾔﾅ|seyana|sorena|そうだよね)")
    if pattern.search(msg.content):
      if client.user != msg.author:
        m = 'わかる'
        await client.send_message(msg.channel, m)

    if re.search(r"クソゲー|くそげー", msg.content) and client.user != msg.author:
      m = 'やめたら？このゲーム'
      await client.send_message(msg.channel, m)

    if re.search(r"どうかな", msg.content) and client.user != msg.author:
      with open('img/wakaru.jpg', 'rb') as f:
        await client.send_file(msg.channel, f)

    if re.search(r"DJRN|djrn|だじ|ダジ|ﾀﾞｼﾞ", msg.content) and client.user != msg.author:
      m = '汚いからやめて'
      await client.send_message(msg.channel, m)

    if re.search(r"(六|6)番ちゃんかわいい", msg.content) and client.user != msg.author:
      m = 'えへへ…'
      await client.send_message(msg.channel, m)


    if msg.content.startswith('!help') and client.user != msg.author:
      await client.send_message(msg.channel, viewHelp())

    if msg.content.startswith('!view_preset') and client.user != msg.author:
      if not msg.attachments:
        await client.send_message(msg.channel, '内容を見たいプリセットをアップしてね')
        def check(msgn):
          return msgn.attachments
        newMsg = await client.wait_for_message(author=msg.author, check=check)
        url = newMsg.attachments[0]['url']
        await client.send_message(msg.channel, viewPreset(url))
      if msg.attachments:
        url = msg.attachments[0]['url']
        await client.send_message(msg.channel, viewPreset(url))

    if msg.content.startswith('!diff_preset') and client.user != msg.author:
      if not msg.attachments:
        await client.send_message(msg.channel, 'ファイルがないよ')
        return
      if msg.attachments:
        originalFileUrl = msg.attachments[0]['url']
        await client.send_message(msg.channel, '比較したいプリセットをアップしてね')
        def check(msgn):
          return msgn.attachments
        newMsg = await client.wait_for_message(author=msg.author, check=check)
        newFileUrl = newMsg.attachments[0]['url']
        await client.send_message(msg.channel, diffPreset(originalFileUrl, newFileUrl))

    if msg.content.startswith('!元ネタ') and client.user != msg.author:
      m = 'https://www.youtube.com/watch?v=OVuYIMa5XBw'
      await client.send_message(msg.channel, m)

  client.run(token)
