import libtorrent as lt
import uuid
import pickle
import codecs
from database_model.model import ActiveTorrents
import os


class Session:

    def __init__(self):
        self._upload_limit = 1
        self._download_limit = -1
        self._session = lt.session()
        self._session.listen_on(6881, 6891)
        self._torrent_handlers = {}
        self._status = ['queued', 'checking', 'downloading metadata',
                        'downloading', 'finished', 'seeding', 'allocating', 'ERROR']
        self._start_downloading_previous_torrents()

    """def save_resume_data(self):
        for torrent_id in self._torrent_handlers:
            a = self._torrent_handlers[torrent_id].save_resume_data()"""

    def listen_alerts(self):
        """#while True:
        alert = self._session.wait_for_alert(10)
        file_completed_alert
        print alert"""

    def pop_alert(self):
        return self._session.pop_alert()

    def pause_all(self):
        self._session.pause()

    def resume_all(self):
        self._session.resume()

    def pause(self, torrent_id):
        self._torrent_handlers[torrent_id].pause()

    def resume(self, torrent_id):
        self._torrent_handlers[torrent_id].resume()

    def add_magnet(self, uri, destination_path):
        ActiveTorrents.create(magnet=uri, download_path=destination_path, status='DOWNLOADING')
        torrent_id = ActiveTorrents.select().order_by(ActiveTorrents.id.desc()).get()
        self._download_from_magnet(torrent_id, uri, destination_path)
        return torrent_id

    def add_torrent(self, torrent_path, destination_path):
        file = str(open(torrent_path, 'rb').read())
        ActiveTorrents.create(
            torrent_file=codecs.encode(file, "base64").decode(),
            download_path=destination_path,
            status='DOWNLOADING'
        )
        torrent_id = ActiveTorrents.select().order_by(ActiveTorrents.id.desc()).get()
        self._download_from_torrent(torrent_id, file, destination_path)
        return torrent_id

    def _start_downloading_previous_torrents(self):
        pass

    def _download_from_magnet(self, torrent_id, uri, destination_path):
        torrent_handler = lt.add_magnet_uri(self._session, uri, {'save_path': destination_path})
        torrent_handler.set_upload_limit(self._upload_limit)
        torrent_handler.set_download_limit(self._download_limit)
        self._torrent_handlers[torrent_id] = torrent_handler

    def _download_from_torrent(self, torrent_id, binary_file, destination_path):
        e = lt.bdecode(binary_file)
        params = {'save_path': destination_path,
                  'storage_mode': lt.storage_mode_t.storage_mode_sparse,
                  'ti': lt.torrent_info(e)}
        torrent_handler = self._session.add_torrent(params)
        self._torrent_handlers[torrent_id] = torrent_handler

    def get_stats(self, id):
        stats = self._torrent_handlers[id].status()
        status = {'progress': stats.progress * 100, 'peers': stats.num_peers, 'seeds': stats.num_seeds,
                  'download_rate': stats.download_rate / 1000, 'upload_rate': stats.upload_rate / 1000,
                  'state': self._status[stats.state]}
        return status


s = Session()

import time
#time.sleep(10)
#magnet = 'magnet:?xt=urn:btih:d8daeb50f386f6d73566f05c11b1a207615e611b&dn=Game.of.Thrones.S07E01.1080p.WEB.h264-TBS&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Fzer0day.ch%3A1337&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969'
#id = s.add_magnet(magnet, "H:\Rulli\proyectos\pepe")
#s.listen_alerts()
id = s.add_torrent('C:\Users\Federico Rulli\Downloads\Phoenix Forgotten (2017) [1080p] [YTS.AG].torrent',
                   'H:\Rulli\proyectos\pepe')




while True:
    print s.get_stats(id)
    time.sleep(1)
    #s.save_resume_data()




