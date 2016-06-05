
import time
import requests
from ctypes import *
#CDLL("/home/federico/Documentos/torrent_cli/libs/libtorrent-rasterbar.so.9.0.0")
import libtorrent as lt
a = requests.get("https://thepiratebay.org/search/Arrow/0/7/0")
ses = lt.session()
ses.listen_on(6881, 6891)

"""
e = lt.bdecode(open("Deadpool (2016) [1080p] [YTS.AG].torrent", 'rb').read())
info = lt.torrent_info(e)

params = { 'save_path': "H:\\pepe", \
        'storage_mode': lt.storage_mode_t.storage_mode_sparse, \
        'ti': info}

h = ses.add_torrent(params)
"""
params = {'save_path': "H:\\pepe", \
          'storage_mode': lt.storage_mode_t.storage_mode_sparse, \
          }

link = "magnet:?xt=urn:btih:d83c61ea0b60b641cf13f61bfbf8095113e9573d&dn=Arrow.S04E23.HDTV.x264-LOL%5Bettv%5D&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969"
h = lt.add_magnet_uri(ses, link, params)
s = h.status()
p=0

while not s.is_seeding:
        s = h.status()
        
        state_str = ['queued', 'checking', 'downloading metadata', \
                'downloading', 'finished', 'seeding', 'allocating']
        print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
                (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                s.num_peers, state_str[s.state])

        time.sleep(1)
        p += 1
        print str(p)



"""
link ="magnet:?xt=urn:btih:6d0da36cb509c795e6fd714ca9b99d7f07d5f71d&dn=the+walking+dead+106+comic+en+espa%26ntilde%3Bol&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969"
from torrent.session import Session
ses = Session()
id = ses.add_magnet('H:\proyecto', link)
#id2 = ses.add_magnet(".", link2)
while True:
    print "arrow"
    status = ses.get_stats(id)
    print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
          (status["progress"], status["download_rate"], status["upload_rate"], status["peers"], status["state"])
    time.sleep(1)
"""