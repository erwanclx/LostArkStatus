import discord
from discord.ext import commands
import os

zones_array = ['NORTH AMERICA WEST', 'NORTH AMERICA EAST', 'EUROPE CENTRAL', 'SOUTH AMERICA', 'EUROPE WEST']
ts = 0
bot = commands.Bot(command_prefix='.')
bot.remove_command('help')
status = dict(
    Good="✅",
    Full="❌",
    Maintenance="⚠️",
    Busy="⛔")

bot.zones_arr = []

async def printall(ctx, text):
    i = 0
    a = []
    b = ""
    index = 0
    for c in text:
        b += c
        i += 1
        split = text.find('\n', i)
        if i == 2000 or (c == '\n' and split > 2000):
            a.append(b)
            i = 0
            index += 2000
            b = ""
    if b != "":
        a.append(b)

    if bot.timer == "":
        for t in a:
            await ctx.send(t)
    else:
        for t in a:
            await ctx.send(t + "\n*Last update : " + bot.timer + "*")

@bot.command()
async def zones(ctx):
    text = ""
    for x in zones_array:
        text += x.title() + '\r\n'
    await printall(ctx, text)

@bot.command()
async def server(ctx, *, entry):
    temp_arr = bot.zones_arr
    temp_arr = [[x for x in v if x['name'].upper() == entry.upper()] for v in temp_arr.values()]
    temp_arr = [x for x in temp_arr if x]
    if temp_arr:
        temp_arr = temp_arr[0][0]
        text = temp_arr["name"] + ': ' + temp_arr["status"] + " " + status[temp_arr["status"]]
    else:
        text = "No server find"

    await printall(ctx, text)

@bot.command()
async def zone(ctx, *, entry):
    arr = bot.zones_arr
    text = ""
    entry = entry.upper()
    if entry in arr.keys():
        for server in arr[entry]:
            text += server["name"] + ": " + server["status"] + " " + status[server["status"]] + "\r\n"
    else:
        text = "No zone find"

    await printall(ctx, text)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Command list :", description="Bot version : v1.2.1", color=15277667)
    embed.add_field(name=".help", value="Show command list", inline=True)
    embed.add_field(name=".zones", value="Show all the zones", inline=True)
    embed.add_field(name=".zone [value]", value="Show the state of the servers of a zone", inline=True)
    embed.add_field(name=".server [value]", value="Show server state", inline=True)
    embed.add_field(name="Server counter :", value=(str(len(bot.guilds))) + " servers.")
    embed.set_thumbnail(url="https://kgo.googleusercontent.com/profile_vrt_raw_bytes_1587514212_1078.jpg")
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name=".devhelp to see commands", url='https://github.com/erwanclx'))


    # -------- LOAD SCRAP FILE -------- #

for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f"cogs.{filename[:-3]}")
        except Exception as e:
            print(e)
bot.run('')