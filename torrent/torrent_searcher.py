from tpb import TPB
from tpb import CATEGORIES, ORDERS
import re


class TorrentSearcher():

    def __init__(self):
        self._pirategateway = TPB('https://thepiratebay.org')

    def search(self, row):
        list = row.split("&")
        name = list[0]
        type = list[1]
        season = list[2]
        chapters = {}
        #if season != "*" and type == "serie":

    def _search_for_serie(self, name, season):
        chapters = {}
        for page in range(0, 10):
            torrents = self._pirategateway.search(name).order(ORDERS.SEEDERS.DES).page(page)
            for torrent in torrents:
                try:
                    file = str(torrent).lower()
                    seas = re.sub(r".*s([0-9]*)e[0-9]*.*", r"\1", file)
                    chapter = re.sub(r".*e([0-9][0-9]).*", r"\1", file)
                    if chapter == file or seas == file:
                        continue
                    if chapter != "" and seas != "" and int(seas) == season:
                        if not chapter in chapters.keys():
                            chapters[chapter] = torrent
                except:
                    continue
        return chapters



s = TorrentSearcher()
a = s._search_for_serie("big bang theory", 9)
a.keys().sort()
for key in a:
    print str(a[key])
