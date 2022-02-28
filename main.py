import discord
from discord.ext import commands
import os

zones_array = ['NORTH AMERICA WEST', 'NORTH AMERICA EAST', 'EUROPE CENTRAL', 'SOUTH AMERICA', 'EUROPE WEST']
ts = 0
bot = commands.Bot(command_prefix='.')
bot.remove_command('help')
status = dict(
  Good = "✅",
  Full = "❌",
  Maintenance = "⚠️",
  Busy = "⛔")
bot.zones_arr = []

@bot.command()
async def zones(ctx):
    text = ""
    for x in zones_array:
        text += x.title() + '\r\n'
    if bot.timer == "":
        embed = discord.Embed(color=15277667)
        embed.add_field(name="All zones available :", value=text, inline=True)
        embed.set_thumbnail(url="https://kgo.googleusercontent.com/profile_vrt_raw_bytes_1587514212_1078.jpg")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=15277667)
        embed.add_field(name="All zones available :", value=text, inline=True)
        embed.set_thumbnail(url="https://kgo.googleusercontent.com/profile_vrt_raw_bytes_1587514212_1078.jpg")
        embed.set_footer(text="Last update : " + bot.timer)
        await ctx.send(embed=embed)

@bot.command()
async def server(ctx, *, entry):
    temp_arr = bot.zones_arr
    temp_arr = [[x for x in v if x['name'].upper() == entry.upper()] for v in temp_arr.values()]
    temp_arr = [x for x in temp_arr if x]
    if temp_arr:
        temp_arr = temp_arr[0][0]
        text = temp_arr["status"] + " " + status[temp_arr["status"]]
    else:
        text = "No server find"
    if bot.timer == "":
        embed = discord.Embed(title=entry + " :", color=15277667)
        embed.add_field(name="Server status :", value=text, inline=True)
        embed.set_thumbnail(url="https://kgo.googleusercontent.com/profile_vrt_raw_bytes_1587514212_1078.jpg")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=entry + " :", color=15277667)
        embed.add_field(name="Server status :", value=text, inline=True)
        embed.set_thumbnail(url="https://kgo.googleusercontent.com/profile_vrt_raw_bytes_1587514212_1078.jpg")
        embed.set_footer(text="Last update : " + bot.timer)
        await ctx.send(embed=embed)

@bot.command()
async def zone(ctx, *, entry):
    arr = bot.zones_arr
    entry = entry.upper()
    servers_status = dict(
        Good=[],
        Full=[],
        Maintenance=[],
        Busy=[]
    )
    if entry in arr.keys():
        for server in arr[entry]:
            servers_status[server['status']].append(server['name'])
    else:
        "No zone find"

    text = servers_status
    if text['Good'] == []:
        text['Good'] = "No server in this status"
    else:
        text['Good'].sort()
        text['Good'] = '\n'.join(text['Good'])

    if text['Full'] == []:
        text['Full'] = "No server in this status"
    else:
        text['Full'].sort()
        text['Full'] = '\n'.join(text['Full'])

    if text['Busy'] == []:
        text['Busy'] = "No server in this status"
    else:
        text['Busy'].sort()
        text['Busy'] = '\n'.join(text['Busy'])

    if text['Maintenance'] == []:
        text['Maintenance'] = "No server in this status"
    else:
        text['Maintenance'].sort()
        text['Maintenance'] = '\n'.join(text['Maintenance'])

    if bot.timer == "":
        embed = discord.Embed(title=entry + " :", color=15277667)
        embed.add_field(name="Good ✅", value=text['Good'], inline=True)
        embed.add_field(name="Full ❌", value=text['Full'], inline=True)
        embed.add_field(name="Busy ⛔", value=text['Busy'], inline=True)
        embed.add_field(name="Maintenance ⚠️", value=text['Maintenance'], inline=True)
        embed.set_thumbnail(url="https://kgo.googleusercontent.com/profile_vrt_raw_bytes_1587514212_1078.jpg")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=entry + " :", color=15277667)
        embed.add_field(name="Good ✅", value=text['Good'], inline=True)
        embed.add_field(name="Full ❌", value=text['Full'], inline=True)
        embed.add_field(name="Busy ⛔", value=text['Busy'], inline=True)
        embed.add_field(name="Maintenance ⚠️", value=text['Maintenance'], inline=True)
        embed.set_footer(text="Last update : " + bot.timer)
        embed.set_thumbnail(url="https://kgo.googleusercontent.com/profile_vrt_raw_bytes_1587514212_1078.jpg")
        await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Command list :", description="Bot version : v1.3", color=15277667)
    embed.add_field(name=".help", value="Show command list", inline=True)
    embed.add_field(name=".zones", value="Show all the zones", inline=True)
    embed.add_field(name=".zone [value]", value="Show the state of the servers of a zone", inline=True)
    embed.add_field(name=".server [value]", value="Show server state", inline=True)
    embed.add_field(name="Server counter :", value=(str(len(bot.guilds))) + " servers.")
    embed.set_thumbnail(url="https://kgo.googleusercontent.com/profile_vrt_raw_bytes_1587514212_1078.jpg")
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name=".help to see commands", url='https://github.com/erwanclx'))


    # -------- LOAD SCRAP FILE -------- #

for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f"cogs.{filename[:-3]}")
        except Exception as e:
            print(e)
bot.run('')