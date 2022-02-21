import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
import os
from datetime import datetime

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

    if timer == "":
        for t in a:
            await ctx.send(t)
    else:
        for t in a:
            await ctx.send(t + "\n*Last update : " + timer + "*")


@bot.command()
async def zones(ctx):
    text = ""
    global timer
    timer = ""
    for x in zones_array:
        text += x.title() + '\r\n'
    await printall(ctx, text)


@bot.command()
async def server(ctx, *, entry):
    global ts
    global zones_arr
    if datetime.timestamp(datetime.now()) - ts < (5 * 60 * 1000):
        zones_arr = []

    zone_class = "ags-ServerStatus-content-responses-response"
    server_class = "ags-ServerStatus-content-responses-response-server"
    server_name_class = "ags-ServerStatus-content-responses-response-server-name"
    server_status_class = "ags-ServerStatus-content-responses-response-server-status"

    URL = "http://playlostark.com/fr-fr/support/server-status"
    page = requests.get(URL)
    page
    page.status_code
    200
    page.content

    soup = BeautifulSoup(page.content, "html.parser")
    zones = soup.find_all("div", class_=zone_class)
    zones_arr = {}

    for zone in zones:
        servers = zone.find_all("div", class_=server_class)
        servers_arr = []
        for server in servers:
            name = server.find("div", class_=server_name_class)
            status = server.find("div", class_=server_status_class)
            server_status = ""
            server_obj = {}
            if ("ags-ServerStatus-content-responses-response-server-status--good") in status.attrs.get("class"):
                server_status = "Good"
            if ("ags-ServerStatus-content-responses-response-server-status--busy") in status.attrs.get("class"):
                server_status = "Busy"
            if ("ags-ServerStatus-content-responses-response-server-status--full") in status.attrs.get("class"):
                server_status = "Full"
            if (("ags-ServerStatus-content-responses-response-server-status--maintenance") in status.attrs.get(
                    "class")):
                server_status = "Maintenance"
            server_obj['name'] = name.text.replace("\n", "").replace("\r", "").replace(" ", "")
            server_obj['status'] = server_status
            servers_arr.append(server_obj)
        zones_arr[(zones_array[int(zone.attrs.get('data-index'))])] = servers_arr
    ts = datetime.timestamp(datetime.now())
    print('refresh')
    print(type(zones_arr))
    print(zones_arr)
    global timer
    hour = str(datetime.now().hour)
    minute = datetime.now().minute
    if minute < 10:
        minute = "0", str(minute)
    timer = hour + "h" + str(minute)
    temp_arr = zones_arr
    temp_arr = [[x for x in v if x['name'].upper() == entry.upper()] for v in temp_arr.values()]
    temp_arr = [x for x in temp_arr if x]
    status = dict(
        Good="✅",
        Full="❌",
        Maintenance="⚠️",
        Busy="⛔")
    if temp_arr:
        temp_arr = temp_arr[0][0]
        text = temp_arr["name"] + ': ' + temp_arr["status"] + " " + status[temp_arr["status"]]
    else:
        text = "No server find"

    await printall(ctx, text)


@bot.command()
async def zone(ctx, *, entry):
    global ts
    global zones_arr
    if datetime.timestamp(datetime.now()) - ts < (5 * 60 * 1000):
        zones_arr = []

    zone_class = "ags-ServerStatus-content-responses-response"
    server_class = "ags-ServerStatus-content-responses-response-server"
    server_name_class = "ags-ServerStatus-content-responses-response-server-name"
    server_status_class = "ags-ServerStatus-content-responses-response-server-status"

    URL = "http://playlostark.com/fr-fr/support/server-status"
    page = requests.get(URL)
    page
    page.status_code
    200
    page.content

    soup = BeautifulSoup(page.content, "html.parser")
    zones = soup.find_all("div", class_=zone_class)
    zones_arr = {}

    for zone in zones:
        servers = zone.find_all("div", class_=server_class)
        servers_arr = []
        for server in servers:
            name = server.find("div", class_=server_name_class)
            status = server.find("div", class_=server_status_class)
            server_status = ""
            server_obj = {}
            if ("ags-ServerStatus-content-responses-response-server-status--good") in status.attrs.get("class"):
                server_status = "Good"
            if ("ags-ServerStatus-content-responses-response-server-status--busy") in status.attrs.get("class"):
                server_status = "Busy"
            if ("ags-ServerStatus-content-responses-response-server-status--full") in status.attrs.get("class"):
                server_status = "Full"
            if (("ags-ServerStatus-content-responses-response-server-status--maintenance") in status.attrs.get(
                    "class")):
                server_status = "Maintenance"
            server_obj['name'] = name.text.replace("\n", "").replace("\r", "").replace(" ", "")
            server_obj['status'] = server_status
            servers_arr.append(server_obj)
        zones_arr[(zones_array[int(zone.attrs.get('data-index'))])] = servers_arr
    ts = datetime.timestamp(datetime.now())
    print('refresh')
    print(type(zones_arr))
    print(zones_arr)
    global timer
    hour = str(datetime.now().hour)
    minute = datetime.now().minute
    if minute < 10:
        minute = "0", str(minute)
    timer = hour + "h" + str(minute)
    arr = zones_arr
    text = ""
    entry = entry.upper()
    status = dict(
        Good="✅",
        Full="❌",
        Maintenance="⚠️",
        Busy="⛔")
    if entry in arr.keys():
        for server in arr[entry]:
            text += server["name"] + ": " + server["status"] + " " + status[server["status"]] + "\r\n"
    else:
        text = "No zone find"

    await printall(ctx, text)


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Listes des commandes", description="", color=15277667)
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
bot.run('')