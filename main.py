import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

from datetime import datetime

zones_array = ['WEST NORTH AMERICA', 'EAST NORTH AMERICA', 'EUROPE', 'SOUTH AMERICA']

zones_arr = {}
ts = 0

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')
status = dict(
  Bien = "✅",
  Occupé = "❌",
  Maintenance = "⚠️",
  Plein = "⛔")


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

    for t in a:
        await ctx.send(t)

@bot.command()
async def zones(ctx):
    text = ""
    for x in zones_array:
        text += x.title() + '\r\n'
    await printall(ctx, text)

@bot.command()
async def serveur(ctx, *, entry):
    temp_arr = serveur_scrape()
    temp_arr = [[x for x in v if x['name'].upper() == entry.upper()] for v in temp_arr.values()]
    temp_arr = [x for x in temp_arr if x]
    if temp_arr:
        temp_arr = temp_arr[0][0]
        text = temp_arr["name"] + ': ' + temp_arr["status"] + " " + status[temp_arr["status"]]
    else:
        text = "Pas de serveur trouvé"

    await printall(ctx, text)

@bot.command()
async def zone(ctx, *, entry):
    arr = serveur_scrape()
    text = ""
    entry = entry.upper()
    if entry in arr.keys():
        for server in arr[entry]:
            text += server["name"] + ": " + server["status"] + " " + status[server["status"]] + "\r\n"
    else:
        text = "Pas de zone trouvée"

    await printall(ctx, text)


def serveur_scrape():
    global zones_arr
    global ts

    if datetime.timestamp(datetime.now()) - ts < (5 * 60 * 1000):
        return zones_arr

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
                server_status = "Bien"
            if ("ags-ServerStatus-content-responses-response-server-status--busy") in status.attrs.get("class"):
                server_status = "Occupé"
            if ("ags-ServerStatus-content-responses-response-server-status--full") in status.attrs.get("class"):
                server_status = "Plein"
            if (("ags-ServerStatus-content-responses-response-server-status--maintenance") in status.attrs.get("class")):
                server_status = "Maintenance"
            server_obj['name'] = name.text.replace("\n", "").replace("\r", "").replace(" ", "")
            server_obj['status'] = server_status
            servers_arr.append(server_obj)
        zones_arr[(zones_array[int(zone.attrs.get('data-index'))])] = servers_arr

    ts = datetime.timestamp(datetime.now())
    return zones_arr

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Listes des commandes", description="", color=15277667)
    embed.add_field(name=".help", value="Voir la liste de toutes les commandes", inline=True)
    embed.add_field(name=".zones", value="Montres la liste de toutes les zones", inline=True)
    embed.add_field(name=".zone [valeur]", value="Montres la liste des serveurs de la zone indiquée avec leur état", inline=True)
    embed.add_field(name=".serveur [valeur]", value="Montres l'état du serveur", inline=True)

    embed.set_thumbnail(url="https://kgo.googleusercontent.com/profile_vrt_raw_bytes_1587514212_1078.jpg")
    await ctx.send(embed=embed)
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name=".help to see commands", url='https://github.com/erwanclx'))
bot.run('OTQyNDA4NDk3NTk1ODEzOTU4.YgkETg.CqeM7QNefBE4Ing3Hgqji-J620g')