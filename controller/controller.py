from torrent.session import Session
from series_manager.series_manager import SeriesManager


class Controller(object):

    def __init__(self):
        self._session = Session()

    def start_downloading(self):