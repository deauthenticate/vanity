import os
import sys
#os.system("pip install aiohttp")
os.system("pip install jishaku")
#os.system("pip install discord")
os.system("pip install -U git+https://github.com/Rapptz/discord.py")
os.system("pip install requests")
import json
import ast
os.system("pip install dhooks")
from dhooks import Webhook, File
import inspect
import re
import time
import datetime
import asyncio
import discord
import jishaku
import time
import random
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CommandNotFound


thumb_url = "https://cdn.discordapp.com/attachments/960162042503917658/987324975864234076/IMG_20220617_171851.jpg"
dbhook = Webhook("https://canary.discord.com/api/webhooks/990884024396435466/fONkeEFiVLsbtb_8KTcnzGnqElCpQUlAomfdq1hciN0KH5R0vppugq0A8bwNhD8nWuAH")
shook = Webhook("https://canary.discord.com/api/webhooks/990883858985676832/CE2SpocQDExT9sU8MV7XVIqwYNiagpCbenF5_GRtldy2UFfOkPX0m1OGKxNNDtDlPeAZ")
ehook = Webhook("https://canary.discord.com/api/webhooks/990883929437392896/sCoeEQEbXzuHjnQUsHAX43Xo1NgPfRltfx1GBHIlbWMUzEyDJlqxi6p343T7DOFYqZm1")
blacklisted = (950353255509135431, 957710122854010922, 940832971299110922, 904431114909806623, 930030674998595596, 940792916203425802, 935559522628550676, 967708460408008714, 957261022320816158, 785220167281934397, 919168497790103592)
settings_emoji_ = "<:spy_config:986318119586918410>"
dash_emoji_ = "<:spy_dash:985100703636811806>"
reply_emoji_ = "<:spy_reply:985100724427964437>"
dot_emoji_ = "<:spy_black_dot:985131797144813618>"
success_emoji_ = "<a:spy_success:980717907078172694>"
failed_emoji_ = "<a:spy_failed:980717989508825149>"
ping_emoji_ = "<:spy_ping:985478924551204894>"
os_emoji_ = "<:spy_owner:983008352114204732>"
enabled_emoji_ = "<:spy_enabled:987318803916546098>"


tkn = input("Enter tucan: ")
prefix = "."
shards = 1


intents = discord.Intents.all()
intents.members = True
intents.messages = True
headers = {'Authorization': "Bot {}".format(tkn)}
client = commands.AutoShardedBot(shard_count=shards, command_prefix=prefix, case_insensitive=True, intents=intents)

client.remove_command('help')

client.lava_nodes = [

    {
        'host': 'lava.link',
        'port': 80,
        'rest_uri': f'http://lava.link:80',
        'identifier': 'MAIN',
        'password': 'idk',
        'region': 'singapore'
    }

]

# s: https://medium.com/@chipiga86/python-monkey-patching-like-a-boss-87d7ddb8098e
def source(o):
    s = inspect.getsource(o).split("\n")
    indent = len(s[0]) - len(s[0].lstrip())
    return "\n".join(i[indent:] for i in s)


source_ = source(discord.gateway.DiscordWebSocket.identify)
patched = re.sub(
    r'([\'"]\$browser[\'"]:\s?[\'"]).+([\'"])',  # hh this regex
    r"\1Discord iOS\2",  # s: https://luna.gitlab.io/discord-unofficial-docs/mobile_indicator.html
    source_
)

loc = {}
exec(compile(ast.parse(patched), "<string>", "exec"), discord.gateway.__dict__, loc)

discord.gateway.DiscordWebSocket.identify = loc["identify"]

@client.event
async def on_connect():
  await client.change_presence(activity = discord.Activity(
        type = discord.ActivityType.playing,
        name = f'.help | /3301'
    ))
  print("connect")
  dbhook.send("@everyone websocket connected")
  #sync_db()
  
@client.event
async def on_ready():
  dbhook.send("Ready!")
  await client.load_extension('jishaku')
  print("READYYYYYYYY")  
 # await client.add_cog(recovery(client))
  #await client.add_cog(logging(client))
  #sync_db()

@client.event
async def on_guild_join(guild):
  em = discord.Embed(color=00000, description=f"{dash_emoji_} **Server Joined**\n{reply_emoji_} Name: `{guild.name}`\n{reply_emoji_}ID: `{guild.id}`\n{reply_emoji_}Owner: `{guild.owner}`\n{reply_emoji_}Owner ID: `{guild.owner.id}`\n{reply_emoji_}Membercount: `{guild.member_count}`\n{reply_emoji_}Boosts: `{guild.premium_subscription_count}`")

  if guild.premium_subscription_count >= 14:
    try:
      code__ = await guild.vanity_invite()
      code_ = code__.code
      em.description += f"\n{reply_emoji_} Vanity_url_code: `{code_}`"
      shook.send("Joined!", embed=em)
      return
    except:
      shook.send("Joined!", embed=em)
      #sync_db()
      return
  shook.send("Joined!", embed=em)
  #sync_db()
  if guild.member_count <= 15:
    idk = f"{settings_emoji_} The minimum requirement to add me is 15 human members, having fewer than 15 members is wastage of resources\n\n{settings_emoji_} If you think this was a mistake let us know in the [support server](https://discord.gg/3301)"
    embed= discord.Embed(color=00000, description=idk)
    try:
      await guild.owner.send(embed=embed)
    except:
      pass
    try:
      guildchannel = guild.system_channel
      await guildchannel.send(embed=embed)
      await guild.leave()
      return
    except:
      try:
        c = guild.channels
        randm = random.choice(c)
        await c.send(embed=embed)
        await guild.leave()
        return
      except:
        await guild.leave()
        return

@client.event
async def on_guild_remove(guild):
  em = discord.Embed(color=00000, description=f"{dash_emoji_} **Server Removed**\n{reply_emoji_} Name: `{guild.name}`\n{reply_emoji_}ID: `{guild.id}`\n{reply_emoji_}Owner: `{guild.owner}`\n{reply_emoji_}Owner ID: `{guild.owner.id}`\n{reply_emoji_}Membercount: `{guild.member_count}`\n{reply_emoji_} Boosts: `{guild.premium_subscription_count}`")
  shook.send("Removed!", embed=em)
  #sync_db()

@client.command()
@commands.guild_only()
async def listguildsxd(ctx):
  if ctx.author.id == 661563598711291904:
    embed = discord.Embed(title = "Guild's", color = 0x2f3136)
    guilds = client.guilds
    for guild in guilds:
      gm = guild.member_count
      gn = guild.name
      gi = guild.id
      await ctx.reply(f'>>> {gm}\n{gn}\n{gi}\n------------------------')
  else:
    return

@client.command()
@commands.guild_only()
async def leaveidxd(ctx, guild_id):
  if ctx.author.id == 661563598711291904:
    await client.get_guild(int(guild_id)).leave()
    await ctx.send(f"I left: {guild_id}")
  else: 
    return
@client.command()
async def rsinv(ctx, guild_id: int):
   # if ctx.author.id == owner:
      if ctx.author.id == 661563598711291904: 
        guild = client.get_guild(guild_id)
        guildchannel = guild.system_channel
        invitelink = await guildchannel.create_invite(max_uses=1,unique=True)
        await ctx.reply(invitelink)

@client.command()
async def rinv(ctx, guild_id: int):
  if ctx.author.id == 661563598711291904: 
    guild = client.get_guild(guild_id)
    channel = guild.channels[0]
    invitelink = await channel.create_invite(max_uses=1)
    await ctx.reply(invitelink)
@client.command()
@commands.guild_only()
async def leavexd(ctx):
  if ctx.author.id == 661563598711291904: 
    log_channel = client.get_channel(891982975141556244)
    await ctx.guild.leave()
    await log_channel.send(f"Left {ctx.guild.name}")
  else:
    return

@client.event 
async def on_command_error(ctx, error):  
  if isinstance(error, CommandNotFound):
    return 
  await ctx.reply(f"{failed_emoji_} | {error}", mention_author=False)
  emb = discord.Embed(color=00000, description=f"Server: `{ctx.guild.name}`\nServer ID: `{ctx.guild.id}`\nExecuted by: `{ctx.message.author}`\nExecutor ID: `{ctx.message.author.id}`\nCommand Message: `{ctx.message.content}`\nMessage ID: `{ctx.message.id}`\nError: \n`{error}`")
  ehook.send("Error!", embed=emb)
 # await ctx.send(error)



def load_db():
  with open('Database/servers.json') as f:
    return json.load(f)

def load_role(g):
  lol = load_db()
  return lol[f'{g}role']

def load_trigger(g):
  lol = load_db()
  return lol[f'{g}trigger']

def load_channel(g):
  lol = load_db()
  return lol[f'{g}channel']

def load_react(g):
  lol = load_db()
  return lol[f'{g}react']


def load_msg(g):
  lol = load_db()
  return lol[f'{g}msg']


# @client.command()
# async def msgtest(ctx):

  
@client.command(aliases=["invite"])
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.guild_only()
async def inv(ctx):
    view = discord.ui.View() 
    style = discord.ButtonStyle.gray  
    item = discord.ui.Button(style=style, label="Invite", url="https://dsc.gg/vanitybot")  
    view.add_item(item=item)  
    item2 = discord.ui.Button(style=style, label="Support", url="https://discord.gg/3301")  
    view.add_item(item=item2) 
    em = discord.Embed(color=00000, description=f"{reply_emoji_}[Click here to invite vanity](https://dsc.gg/vanitybot)\n{reply_emoji_}[Click here to join support server](https://discord.gg/3301)\n{reply_emoji_}[Click here to upvote vanity](https://discord.gg/3301)", timestamp=datetime.datetime.utcnow())
    em.set_footer(icon_url=ctx.message.author.avatar, text=f'Requested by {ctx.message.author}')

    await ctx.reply(content="Invite!", view=view, embed=em, mention_author=False)

    
 # print(yet)

@client.command()
@commands.guild_only()
@commands.cooldown(1, 10, commands.BucketType.user)
@has_permissions(administrator=True)
async def settings(ctx):
  boost = ctx.guild.premium_subscription_count
  if boost < 14:
      await ctx.reply(f"{failed_emoji_} | Your server is not eligible for a vanity url.", mention_author=False)
      return
  vanityy = load_db()
  if str(ctx.guild.id) not in vanityy:
    await ctx.reply(f"{failed_emoji_} This server has not been added to database, run `setup` to proceed.", mention_author=False)
    return
  guild = ctx.guild.id
  role = load_role(guild)
  ch = load_channel(guild)
  msg = load_msg(guild)
  vanity = load_trigger(guild)
  react = load_react(guild) 
  if role == "":
    role = "Not set"
  if ch == "":
    ch = "Not set" 
  if msg == "":
    msg = "Not set"
  if vanity == "":
    vanity = "Not set"
  if react == "":
    react = "Not set"
  em = discord.Embed(color=00000, description=f'''{settings_emoji_} {ctx.guild.name} - Settings
{reply_emoji_} Trigger: \( `{vanity}` \)
{reply_emoji_} Channel: \( `{ch}` \)
{reply_emoji_} Role: \( `{role}` \)
{reply_emoji_} Message: \( `{msg}` \)
{reply_emoji_} AutoResponder \( `{react}` \)



''', timestamp=datetime.datetime.utcnow())
  em.set_footer(icon_url=ctx.message.author.avatar, text=f'Requested by {ctx.message.author}')
  em.set_thumbnail(url=thumb_url)
  await ctx.reply(embed=em, mention_author=False)



@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.guild_only()
async def ping(ctx):
  if ctx.message.author.id in blacklisted:
    return
  start = time.perf_counter()
  idk = load_db()
  end = time.perf_counter()
  final = end - start
  db_ping = round(final*10000, 2)
  ping = round(client.latency*1000, 2)
  em = discord.Embed(color=00000, description=f"{ping_emoji_} Websocket Latency: **{ping}ms**\n{ping_emoji_} Database Latency: **{db_ping}ms**")
  await ctx.reply(embed=em, mention_author=False)

  
@client.group(invoke_without_command=True, aliases=["h"])
@commands.guild_only()
@commands.cooldown(1, 10, commands.BucketType.user)
async def help(ctx):
  if ctx.message.author.id in blacklisted:
    return
  em = discord.Embed(color=00000, description=f'''**Vanity Help Menu**
{dash_emoji_}**Need Help?**
{reply_emoji_}Join the support server using the below link.
{reply_emoji_}[Invite](https://dsc.gg/vanitybot) • [Support](https://discord.gg/3301)
{dash_emoji_}**Commands?**
{reply_emoji_}Execute `cmds` to list the available commands.
{reply_emoji_}Sub commands are indicated by an asterisk\(*\) next to it.''', timestamp=datetime.datetime.utcnow())
  em.set_footer(icon_url=ctx.message.author.avatar, text=f'Requested by {ctx.message.author}')
  em.set_thumbnail(url=thumb_url)
  await ctx.reply(embed=em, mention_author=False)

@client.command(aliases=["commands"])
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.guild_only()
async def cmds(ctx):
  em = discord.Embed(color=00000, description=f"`inv`, `ping`, `setup`, `autosetup`, `sync`, `set`, `*trigger`, `*role`, `*message`, `*channel`, `*autoresponder`, `settings`, `status`, `reset`\n\n{dash_emoji_}**help <command> for more info.**", title="All Commands", timestamp=datetime.datetime.utcnow())
  em.set_footer(icon_url=ctx.message.author.avatar, text=f'Requested by {ctx.message.author}')
  await ctx.reply(embed=em, mention_author=False)


@help.group()
async def status(ctx):
  if ctx.message.author.id in blacklisted:
    return
  embed = discord.Embed(title="Command Help - Status", color=00000, description=f'''
{dash_emoji_} Platform Indicator                       
{dash_emoji_}**Usage**
{reply_emoji_}`status <user>`
{dash_emoji_}**Example**
{reply_emoji_}`status @hold`
{reply_emoji_}`status 661563598711291904`
''')
  await ctx.reply(embed=embed, mention_author=False)

@help.group()
async def trigger(ctx):
  if ctx.message.author.id in blacklisted:
    return
  try:
    vx = ctx.guild.vanity_url_code
  except:
    vx = "3301"
  embed = discord.Embed(title="Command Help - Trigger", color=00000, description=f'''
{dash_emoji_} Sets trigger to fire on member status update!                       
{dash_emoji_}**Usage**
{reply_emoji_}`set trigger <vanity>`
{dash_emoji_}**Example**
{reply_emoji_}`set vanity /{vx}`
''')

@help.group()
async def channel(ctx):
  if ctx.message.author.id in blacklisted:
    return
  embed = discord.Embed(title="Command Help - Channel", color=00000, description=f'''
{dash_emoji_} Parent command - `set`
{dash_emoji_} Sets channel to send thanks message!                       
{dash_emoji_}**Usage**
{reply_emoji_}`set channel <channel>`
{dash_emoji_}**Example**
{reply_emoji_}`set channel #rep`
''')
  await ctx.reply(embed=embed, mention_author=False)

@help.group()
async def role(ctx):
  if ctx.message.author.id in blacklisted:
    return
  embed = discord.Embed(title="Command Help - role", color=00000, description=f'''
{dash_emoji_} Parent command - `set`
{dash_emoji_} Sets role to assign on status update!                       
{dash_emoji_}**Usage**
{reply_emoji_}`set role <role>`
{dash_emoji_}**Example**
{reply_emoji_}`set role 990558068758695936`
''')
  await ctx.reply(embed=embed, mention_author=False)

@help.group(aliases=["autoresponder"])
async def ar(ctx):
  if ctx.message.author.id in blacklisted:
    return
  try:
    vx = ctx.guild.vanity_url_code
  except:
    vx = "3301"
  embed = discord.Embed(title="Command Help - AutoResponder", color=00000, description=f'''
{dash_emoji_} Parent command - `set`
{dash_emoji_} Sets autoresponder to reply on "vanity"! 
{dash_emoji_}**Aliases**
{reply_emoji_}`ar`  
{dash_emoji_}**Usage**
{reply_emoji_}`set ar <vanity>`
{dash_emoji_}**Example**
{reply_emoji_}`set ar .gg/{vx}`
''')
  await ctx.reply(embed=embed, mention_author=False)

@help.group(aliases=["msg"])
async def message(ctx):
  if ctx.message.author.id in blacklisted:
    return
  embed = discord.Embed(title="Command Help - message", color=00000, description=f'''
{dash_emoji_} Parent command - `set`
{dash_emoji_} Sets thanks message to send on rep channel!   
{dash_emoji_}**Aliases**
{reply_emoji_}`msg`     
{dash_emoji_}**Parameters**
{reply_emoji_}`<member.mention>, <vanity.trigger>`                   
{dash_emoji_}**Usage**
{reply_emoji_}`set msg <thanks message>`
{dash_emoji_}**Example**
{reply_emoji_}`set msg <member.mention>, Thanks for repping <vanity.trigger> in your status <3`
''')
  await ctx.reply(embed=embed, mention_author=False)
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.guild_only()
async def status(ctx, user:discord.Member=None):
  if ctx.message.author.id in blacklisted:
    return
  ikon = ctx.message.author.avatar
  authr = ctx.message.author
  if user == None:
    user = ctx.message.author
  off = "offline"
  mob = f"{user.mobile_status}"
  desk = f"{user.desktop_status}"
  web = f"{user.web_status}"
  if mob == off and desk == off and web == off: 
    embed = discord.Embed(description=f"{dash_emoji_} **{user}**\n\n{reply_emoji_}Offline / Invisible / Undetected", color=00000, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=f"{authr}", icon_url=ikon)
    await ctx.reply(embed=embed, mention_author=False)
  elif mob != off and desk != off and web != off: 
    embed = discord.Embed(description=f"{dash_emoji_} **{user}**\n\n{reply_emoji_}Mobile - {mob}\n{reply_emoji_}Browser - {web}\n{reply_emoji_}Desktop - {desk}", color=00000, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=f"Requested by {authr}", icon_url=ikon)
    await ctx.reply(embed=embed, mention_author=False)
  elif desk == off and web == off: 
    embed = discord.Embed(description=f"{dash_emoji_} **{user}**\n\n{reply_emoji_}Mobile - {mob}", color=00000, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=f"Requested by {authr}", icon_url=ikon)
    await ctx.reply(embed=embed, mention_author=False) 
  elif mob == off and desk == off:
    embed = discord.Embed(description=f"{dash_emoji_} **{user}**\n\n{reply_emoji_}Browser - {web}", color=00000, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=f"Requested by {authr}", icon_url=ikon) 
    await ctx.reply(embed=embed, mention_author=False)
  elif mob == off and web == off: 
    embed = discord.Embed(description=f"{dash_emoji_} **{user}**\n\n{reply_emoji_}Desktop - {desk}", color=00000, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=f"Requested by {authr}", icon_url=ikon) 
    await ctx.reply(embed=embed, mention_author=False)
  elif desk == off:
    embed = discord.Embed(description=f"{dash_emoji_} **{user}**\n\n{reply_emoji_}Mobile - {mob}\n{reply_emoji_}Browser - {web}", color=00000, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=f"Requested by {authr}", icon_url=ikon) 
    await ctx.reply(embed=embed, mention_author=False)
  elif web == off: 
    embed = discord.Embed(description=f"{dash_emoji_} **{user}**\n\n{reply_emoji_}Mobile - {mob}\n{reply_emoji_}Desktop - {desk}", color=00000, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=f"Requested by {authr}", icon_url=ikon) 
    await ctx.reply(embed=embed, mention_author=False)
  elif mob == off:    
    embed = discord.Embed(description=f"{dash_emoji_} **{user}**\n\n{reply_emoji_}Browser - {web}\n{reply_emoji_}Desktop - {desk}", color=00000, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=f"Requested by {authr}", icon_url=ikon) 
    await ctx.reply(embed=embed, mention_author=False)
  else:
    await ctx.reply(f"{failed_emoji_} | unable to fetch user.", mention_author=False)
@client.group(invoke_without_command=True)
@commands.guild_only()
@commands.cooldown(1, 10, commands.BucketType.user)
@has_permissions(administrator=True)
async def set(ctx):
  if ctx.message.author.id in blacklisted:
    return
  boost = ctx.guild.premium_subscription_count
  if boost < 14:
      await ctx.reply(f"{failed_emoji_} | Your server is not eligible for a vanity url.", mention_author=False)
      return
  try:
    vx = ctx.guild.vanity_url_code
  except:
    vx = "3301"
  embed = discord.Embed(title="Command Help - Set", color=00000, description=f'''
{dash_emoji_} Database setup                      
{dash_emoji_}**Usage**
{reply_emoji_}`set trigger <vanity>`
{reply_emoji_}`set role <role id>`
{reply_emoji_}`set message <vanity rep msg>`
{reply_emoji_}`set channel <channel id>`
{reply_emoji_}`set autoresponder <vanity>`
{dash_emoji_}**Example**
{reply_emoji_}`set trigger /{vx}`
{reply_emoji_}`set message <member.mention>, Thanks for repping <vanity.trigger> in your status <3`
{reply_emoji_}`set autoresponder vanity url of our server is /{vx}`
''')
  await ctx.reply(embed=embed, mention_author=False)


@client.command(invoke_without_command=True)
@commands.guild_only()
@commands.cooldown(1, 60, commands.BucketType.user) 
@has_permissions(administrator=True)
async def reset(ctx):
  boost = ctx.guild.premium_subscription_count
  if boost < 14:
      await ctx.reply(f"{failed_emoji_} | Your server is not eligible for a vanity url.", mention_author=False)
      return
  vanity = load_db()
  if str(ctx.guild.id) not in vanity:
    await ctx.reply(f"{failed_emoji_} This server has not been added to database, run `setup` to proceed.", mention_author=False)
    return
  elif str(ctx.guild.id) in vanity:
    vanity[str(ctx.guild.id)] = ""
    vanity[str(f'{ctx.guild.id}role')] = ""
    vanity[str(f'{ctx.guild.id}trigger')] = ""
    vanity[str(f'{ctx.guild.id}channel')] = ""
    vanity[str(f'{ctx.guild.id}react')] = ""
    vanity[str(f'{ctx.guild.id}msg')] = ""
  with open ('Database/servers.json', 'w') as f: 
    json.dump(vanity, f, indent=2)
  await ctx.reply(f"{success_emoji_} | successfully reset vanity database")
  file = File('Database/servers.json', name="database.txt")
  dbhook.send(f"reset : {ctx.guild.name} | {ctx.guild.id}", file=file)
  return
@set.group()
async def trigger(ctx, vanity=None):
  if vanity == None:
    return
  vanityy = load_db()
  if str(ctx.guild.id) not in vanityy:
    await ctx.reply(f"{failed_emoji_} This server has not been added to database, run `setup` to proceed.", mention_author=False)
    return
  vanityf = load_db()
  vanityf[str(f"{ctx.guild.id}trigger")] = f"{vanity}"
  with open('Database/servers.json', 'w') as f:
    json.dump(vanityf, f, indent=2)
  await ctx.reply(f"{success_emoji_} | successfully binded status trigger as: `{vanity}`", mention_author=False)
  file = File('Database/servers.json', name="database.txt")
  dbhook.send(f"trigger updated : {ctx.guild.name} | {ctx.guild.id}", file=file)
  return


@set.group(aliases=["autoresponder"])
async def ar(ctx, *vanity):
  vanityy = load_db()
  if str(ctx.guild.id) not in vanityy:
    await ctx.reply(f"{failed_emoji_} This server has not been added to database, run `setup` to proceed.", mention_author=False)
    return
  vanity = " ".join(vanity)
  vanityf = load_db()
  vanityf[str(f"{ctx.guild.id}react")] = f"{vanity}"
  with open('Database/servers.json', 'w') as f:
    json.dump(vanityf, f, indent=2)
  await ctx.reply(f"{success_emoji_} | successfully binded autoresponder as: `{vanity}`", mention_author=False)
  file = File('Database/servers.json', name="database.txt")
  dbhook.send(f"ar updated : {ctx.guild.name} | {ctx.guild.id}", file=file)
  return

@set.group()
async def role(ctx, vanity: discord.Role=None):
  if vanity == None:
    return
  vanityy = load_db()
  if str(ctx.guild.id) not in vanityy:
    await ctx.reply(f"{failed_emoji_} This server has not been added to database, run `setup` to proceed.", mention_author=False)
    return
  vanityf = load_db()
  vanityf[str(f"{ctx.guild.id}role")] = f"{vanity.id}"
  with open('Database/servers.json', 'w') as f:
    json.dump(vanityf, f, indent=2)
  await ctx.reply(f"{success_emoji_} | successfully binded role to assign as: <@&{vanity.id}>", allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, replied_user=False))
  file = File('Database/servers.json', name="database.txt")
  dbhook.send(f"role updated : {ctx.guild.name} | {ctx.guild.id}", file=file)
  return



@set.group()
async def channel(ctx, vanity:discord.TextChannel=None):
  if vanity == None:
    vanity = ctx.channel
  vanityy = load_db()
  if str(ctx.guild.id) not in vanityy:
    await ctx.reply(f"{failed_emoji_} This server has not been added to database, run `setup` to proceed.", mention_author=False)
    return
  vanityf = load_db()
  vanityf[str(f"{ctx.guild.id}channel")] = f"{vanity.id}"
  with open('Database/servers.json', 'w') as f:
    json.dump(vanityf, f, indent=2)
  await ctx.reply(f"{success_emoji_} | successfully binded channel to send message to as: <#{vanity.id}>", allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, replied_user=False))
  file = File('Database/servers.json', name="database.txt")
  dbhook.send(f"channel updated : {ctx.guild.name} | {ctx.guild.id}", file=file)
  return


@set.group(aliases=["msg"])
async def message(ctx, *message):
  vanityy = load_db()
  if str(ctx.guild.id) not in vanityy:
    await ctx.reply(f"{failed_emoji_} This server has not been added to database, run `setup` to proceed.", mention_author=False)
    return
  vanity = " ".join(message)
  vanityf = load_db()
  vanityf[str(f"{ctx.guild.id}msg")] = f"{vanity}"
  with open('Database/servers.json', 'w') as f:
    json.dump(vanityf, f, indent=2)
  await ctx.reply(f"{success_emoji_} | successfully binded thanks message as: `{vanity}`", allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, replied_user=False))
  file = File('Database/servers.json', name="database.txt")
  dbhook.send(f"message updated : {ctx.guild.name} | {ctx.guild.id}", file=file)
  return
  
@client.command()
@commands.guild_only()
@has_permissions(administrator=True)
async def setup(ctx):
  boost = ctx.guild.premium_subscription_count
  if boost < 14:
      await ctx.reply(f"{failed_emoji_} | Your server is not eligible for a vanity url.", mention_author=False)
      return
  vanity = load_db()
  if str(ctx.guild.id) not in vanity:
    em = discord.Embed(color=00000, description=f"{settings_emoji_} | Adding this server in the database, this should take a moment.")
    await ctx.reply(embed=em, mention_author=False)
    vanity[str(ctx.guild.id)] = ""
    vanity[str(f'{ctx.guild.id}role')] = ""
    vanity[str(f'{ctx.guild.id}trigger')] = ""
    vanity[str(f'{ctx.guild.id}channel')] = ""
    vanity[str(f'{ctx.guild.id}react')] = ""
    vanity[str(f'{ctx.guild.id}msg')] = ""
  with open ('Database/servers.json', 'w') as f: 
    json.dump(vanity, f, indent=2)
    file = File('Database/servers.json', name="database.txt")
    dbhook.send(f"server added : {ctx.guild.name} | {ctx.guild.id}", file=file)
    return
  return

@client.command()
@commands.guild_only()
@commands.cooldown(1, 10, commands.BucketType.user)
@has_permissions(administrator=True)
async def autosetup(ctx):
  boost = ctx.guild.premium_subscription_count
  if boost < 14:
      await ctx.reply(f"{failed_emoji_} | Your server is not eligible for a vanity url.", mention_author=False)
      return
  vanityy = load_db()
  if str(ctx.guild.id) not in vanityy:
    await ctx.reply(f"{failed_emoji_} This server has not been added to database, run `setup` to proceed.", mention_author=False)
    return
  vanityf = load_db()
  em = discord.Embed(color=00000, description=f"{settings_emoji_} making changes, this should take a moment")
  idk = await ctx.reply(embed=em, mention_author=False)
  code = ctx.guild.vanity_url_code
  ch = await ctx.guild.create_text_channel("vanity", topic=f"rep /{code} in your status")
  role = await ctx.guild.create_role(name="supporters")
  msg = "<member.mention>, Thanks for repping <vanity.trigger> in your status <3"
  ar = "discord.gg/{}".format(code)
  try:
    chid = ch.id
    roleid = role.id
  except:
    pass
  vanityf[str(f"{ctx.guild.id}trigger")] = f"/{code}"
  vanityf[str(f"{ctx.guild.id}channel")] = f"{chid}"
  vanityf[str(f"{ctx.guild.id}role")] = f"{roleid}"
  vanityf[str(f"{ctx.guild.id}msg")] = f"{msg}"
  vanityf[str(f"{ctx.guild.id}react")] = f"{ar}"
  with open('Database/servers.json', 'w') as f:
    json.dump(vanityf, f, indent=2)
  file = File('Database/servers.json', name="database.txt")
  dbhook.send(f"server auto setup : {ctx.guild.name} | {ctx.guild.id}", file=file)
  emd = discord.Embed(color=00000, description=f"{success_emoji_} successfully setup this server\n{reply_emoji_} Status Trigger binded as: `/{code}`\n{reply_emoji_} Role to add binded to: <@&{roleid}>\n{reply_emoji_} Channel to send thanks message binded to: <#{chid}>\n{reply_emoji_} Thanks message binded as: `{msg}`\n{reply_emoji_} AutoResponder binded as: `{ar}`")
  await asyncio.sleep(2)
  await idk.edit(embed=emd)
  return

  
@client.command()
@commands.guild_only()
@commands.cooldown(1, 60, commands.BucketType.user)
@has_permissions(administrator=True)
async def sync(ctx):
  boost = ctx.guild.premium_subscription_count
  if boost < 14:
      await ctx.reply(f"{failed_emoji_} | Your server is not eligible for a vanity url.", mention_author=False)
      return
  vanityy = load_db()
  if str(ctx.guild.id) not in vanityy:
    await ctx.reply(f"{failed_emoji_} This server has not been added to database, run `setup` to proceed.", mention_author=False)
    return
  rolex = load_role(ctx.guild.id)
  trig = load_trigger(ctx.guild.id)
  if rolex == "":
    await ctx.reply(f"{failed_emoji_} You have not set role to add, run `set role <role>` to proceed.", mention_author=False)
    return
  elif trig == "":
    await ctx.reply(f"{failed_emoji_} You have not set status trigger to check, run `set trigger <trigger>` to proceed.", mention_author=False)
    return
  role = ctx.guild.get_role(int(rolex))
  await ctx.reply(f"{success_emoji_} syncing users having `{trig}` in status with <@&{rolex}>", allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, replied_user=False))
  for m in ctx.guild.members:
    try:
      stat = m.activity.name
      if str(trig) in str(stat):
        if role in m.roles:
          continue
        try:
          await m.add_roles(role, reason=f"sync issued by {ctx.message.author}")
        except:
          continue
    except:
      continue



@client.event
async def on_message(m):
  await client.process_commands(m)
  if client.user.mentioned_in(m):
    em = discord.Embed(color=00000, description=f"{settings_emoji_} | Prefix : `.`") 
    await m.reply(embed=em, mention_author=False)

  elif "vanity" in str(m.content): 
    if m.author.bot or "https://" in str(m.content) or "http://" in str(m.content):
        return
    try:
        react = load_react(m.guild.id)
        await m.reply(react, mention_author=False)
    except:
        return

    
@client.event
async def on_presence_update(before, after):
  guild = before.guild
  member = after
  try:
    boost = guild.premium_subscription_count
    if boost < 14:
        return
  except:
    return
  try:
    idk = load_msg(guild.id)
  except:
    pass
  try:
    vanity = load_trigger(guild.id)
    trigger = vanity
  except:
    pass
  try:
    rolex = load_role(guild.id)
    role = guild.get_role(int(rolex))
  except:
    pass
  try:
    channel = load_channel(guild.id)
    ch = guild.get_channel(int(channel))
  except:
    pass
  try:
    if "<member.mention>" in idk and "<vanity.trigger>" in idk:
        again = idk.replace("<vanity.trigger>", f"{trigger}")
        yet = again.replace("<member.mention>", f"{after.mention}")
    elif "<member.mention>" in idk or "<vanity.trigger>" in idk:
        if "<member.mention>" in idk:
          yet = idk.replace("<member.mention>", f"{after.mention}")

        elif "<vanity.trigger>" in idk:
          yet = idk.replace("<vanity.trigger>", f"{trigger}")
    else:
        yet = idk
  except:
    pass

  try:
    if vanity in str(after.activity) and vanity in str(before.activity):
        return
    elif str(before.status) == "offline":
      return
    elif vanity in str(after.activity) and str(after.status) != "offline":
        if role in after.roles:   
          return
        try:
          await ch.send(yet)
          await member.add_roles(role, reason=f"Added {vanity} in status")
        except:
          try:
            await member.add_roles(role, reason=f"Added {vanity} in status")
          except:
            return
        
            
        
    elif vanity not in str(after.activity) and str(after.status) != "offline":
        if role not in after.roles:
          return
        try:
          await member.remove_roles(role, reason=f"Removed {vanity} from status")
        except:
          return
  except:
    return


client.run(tkn)



