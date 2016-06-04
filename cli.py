from ctypes import *
a=CDLL("./libs/libtorrent-rasterbar.so.9.0.0")
import libtorrent as lt
import time
#ses = lt.session()
#ses.listen_on(6881, 6891)
params={'save_path':'.'}

#h = ses.add_torrent(params)
link="magnet:?xt=urn:btih:c1465e6b7e6a8639007cc67748a37bc52ca0d035&dn=Arrow+S04E21+2016+HDTV+x264+-+TiTAN&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969"
link2 ="magnet:?xt=urn:btih:6d0da36cb509c795e6fd714ca9b99d7f07d5f71d&dn=the+walking+dead+106+comic+en+espa%26ntilde%3Bol&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969"
"""
h = lt.add_magnet_uri(ses,link, params)
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
        if p == 50 :
            ses.pause()
        p += 1
        print 'jajjajajjajajajaj' + str(p)
        if p == 60:
            ses.resume()

"""

from torrent.session import Session
ses = Session()
id = ses.add_magnet(".", link)
id2 = ses.add_magnet(".", link2)
while True:
    print "arrow"
    status = ses.get_stats(id)
    print str(status)
    print "woking"
    status = ses.get_stats(id2)
    print status
    time.sleep(1)