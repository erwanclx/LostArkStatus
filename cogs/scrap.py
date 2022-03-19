import requests
from bs4 import BeautifulSoup
from datetime import datetime
from discord.ext import commands, tasks
import tracemalloc

tracemalloc.start()

zones_array = ['NORTH AMERICA WEST', 'NORTH AMERICA EAST', 'EUROPE CENTRAL', 'EUROPE WEST', 'SOUTH AMERICA']

zones_arr = {}
ts = 0


class scrape_loop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.serveur_scrape.start()

    @tasks.loop(seconds=30)
    async def serveur_scrape(self):
        global zones_arr
        global ts

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
        global timer
        hour = str(datetime.now().hour)
        minute = datetime.now().minute
        if minute < 10:
            minute = "0" + str(minute)
        timer = hour + "h" + str(minute)
        self.bot.timer = timer
        self.bot.zones_arr = zones_arr

#
def setup(bot):
    bot.add_cog(scrape_loop(bot))