import discord
import os
import datetime
from replit import db
import pytz

IST = pytz.timezone('Asia/Kolkata')

client = discord.Client()

def add_spawn_day(author_name,author_id,spawn_day):
  converted_day = str(datetime.datetime.strptime(spawn_day,"%d %B %Y"))
  db[author_id] = converted_day
  print("added",author_name,db[author_id])

def check_spawn_day(author_id):
  return db[author_id]

def update_spawn_day(author_id,new_spawn_day):
  converted_day = str(datetime.datetime.strptime(new_spawn_day,"%d %B %Y"))
  db[author_id] = converted_day
  print("updated..  ",author_id,db[author_id])

def delete_spawn_day(author_id):
  del db[author_id]
  print("deleted.. ",author_id)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  msg = message.content
  if message.author == client:
    return  

  if message.content.startswith('~spawnday new'):
    new_spawn_author = str(message.author)
    new_spawn_author_id = str(new_spawn_author.split('#',1)[1])
    spawn_day = str(msg.split('~spawnday new ',1)[1])
    print(new_spawn_author,new_spawn_author_id,spawn_day)

    if not(new_spawn_author_id in db.keys()):
      print("adding ",new_spawn_author,spawn_day)
      add_spawn_day(new_spawn_author,new_spawn_author_id,spawn_day)
      await message.channel.send('data added to database')

    else:
      print("already existing ")
      value = db[new_spawn_author_id]
      print(value)
      await message.channel.send('The person already exist in our database, try updating the info.')
  
  if message.content.startswith('~spawnday check'):
    spawn_author = str(message.author)
    spawn_author_id = str(spawn_author.split('#',1)[1])
    if spawn_author_id in db.keys():
      print("checking....", spawn_author)
      spawn_day = check_spawn_day(spawn_author_id)[:-8]
      format = "%Y-%m-%d "
      datetime_obj = datetime.datetime.strptime(spawn_day,format)
      spawn_day_converted = datetime_obj.strftime("%dth %B, %Y")
      await message.channel.send(message.author.mention+" was spawned on "+spawn_day_converted)
    else:
      await message.channel.send("The person didn't spawn yet")
  
  if message.content.startswith('~spawnday update'):
    spawn_author = str(message.author)
    spawn_author_id = str(spawn_author.split('#',1)[1])
    new_spawn_day = str(msg.split('~spawnday update ',1)[1])
    if spawn_author_id in db.keys():
      print("updating....", spawn_author,new_spawn_day)
      update_spawn_day(spawn_author_id,new_spawn_day)
      await message.channel.send('data added to database')
    else:
      await message.channel.send("The person didn't spawn yet")
      add_spawn_day(spawn_author,spawn_author_id,new_spawn_day)
      await message.channel.send("The person spawn info was added")
  
  if message.content.startswith("~spawnday delete"):
    spawn_author = str(message.author)
    spawn_author_id = str(spawn_author.split('#',1)[1])
    if spawn_author_id in db.keys():
      print("deleting....", spawn_author)
      delete_spawn_day(spawn_author_id)
      await message.channel.send('data deleted from database')
    else:
      await message.channel.send("The person didn't spawn yet")

client.run(os.getenv('TOKEN'))
# message.author = user_name#id

#todo
#check if today is birthday
