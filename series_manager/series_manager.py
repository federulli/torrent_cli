from database_model.model import *
from series_exceptions.duplicated_serie_exception import DuplicatedSerieException
from torrent.torrent_searcher import TorrentSearcher


class SeriesManager(object):

    def add_series(self, name, download_path):
        try:
            series_id = Series.select().count() + 1
            Series.create(series_id=series_id, name=name, download_path=download_path)
            return series_id
        except Exception:
            raise DuplicatedSerieException()

    def add_season(self, series_id, season_number, episodes_count):
        season_id = Seasons.select().count() + 1
        Seasons.create(
            season_id=season_id,
            series_id=series_id,
            season_number=season_number,
            chapters=episodes_count
            )
        return season_id

    """
    chapter_id = peewee.BigIntegerField(primary_key=True)
    number = peewee.BigIntegerField()
    season_id = peewee.ForeignKeyField(Seasons)
    has_subtitles = peewee.BooleanField(default=False)
    status = peewee.ForeignKeyField(ChapterStatus)
    uri = peewee.CharField(unique=True)
    """

    def add_chapters(self, season_id):
        season_serie = Seasons.select(Seasons.season_number, Seasons.chapters, Series.name).join(Series).\
            where(Seasons.season_id == season_id).naive()[0]
        chapters_uri = TorrentSearcher().search_for_serie(season_serie.name, season_serie.season_number)
        chapter_id = Chapters.select().count()
        for chapter_number in range(1, season_serie.chapters + 1):
            torrent = chapters_uri.get(chapter_number)
            Chapters.create(
                chapter_id=chapter_id + chapter_number,
                number=chapter_number,
                season_id=season_id,
                has_subtitles=False,
                status='READY TO DOWNLOAD' if torrent else 'NOT FOUND',
                uri=torrent.magnet_link if torrent else None
            )



a = SeriesManager().add_series("preacher", 'c')
b = SeriesManager().add_season(a, 2, 13)
SeriesManager().add_chapters(b)