from torrent.session import Session
from series_manager.series_manager import SeriesManager


class Controller(object):

    def __init__(self):
        self._session = Session()
        self._series_manager = SeriesManager()

    def start_downloading(self):
        pass