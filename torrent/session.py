import libtorrent as lt
import uuid
import os

class Session:

    def __init__(self):
        self._session = lt.session()
        self._session.listen_on(6881, 6891)
        self._torrent_handlers = {}
        self.__status = ['queued', 'checking', 'downloading metadata',
                         'downloading', 'finished', 'seeding', 'allocating']

    def add_magnet(self, dest_path, uri):
        # devuelve el urid asignado
        if not os.path.isdir(dest_path):
            raise Exception("No existe el directorio %s" % dest_path)
        id = uuid.uuid1()
        torrent_handler = lt.add_magnet_uri(self._session, uri, {'save_path': dest_path})
        self._torrent_handlers[id] = torrent_handler
        return id

    def get_stats(self, id):
        stats = self._torrent_handlers[id].status()
        status = {'progress': stats.progress * 100, 'peers': stats.num_peers, 'seeds': stats.num_seeds,
                  'download_rate': stats.download_rate / 1000, 'upload_rate': stats.upload_rate / 1000,
                  'state': self.__status[stats.state]}
        return status





