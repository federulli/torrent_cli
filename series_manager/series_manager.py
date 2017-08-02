from database_model.model import *
from series_exceptions.duplicated_serie_exception import DuplicatedSerieException
from torrent.torrent_searcher import TorrentSearcher
import os


class SeriesManager(object):

    @staticmethod
    def add_series(name, download_path):
        try:
            Series.create(name=name, download_path=download_path)
            return Series.get(name=name).id
        except Exception:
            raise DuplicatedSerieException()

    @staticmethod
    def get_ready_to_download():
        chapters = Chapters.select(Chapters.id, Seasons.season_number, Series.download_path, Chapters.uri).join(Seasons).join(Series).where(Chapters.status == 'READY TO DOWNLOAD').naive()
        return [dict(id=chapter.id,
                     path=os.path.join(chapter.download_path, str(chapter.season_number)),
                     uri=chapter.uri) for chapter in chapters]

    @staticmethod
    def add_season(series_id, season_number, episodes_count):
        Seasons.create(
            series_id=series_id,
            season_number=season_number,
            chapters=episodes_count
            )
        return Seasons.get(series_id=series_id, season_number=season_number, chapters=episodes_count).id

    @staticmethod
    def add_chapters(season_id):
        season_serie = Seasons.select(Seasons.season_number, Seasons.chapters, Series.name).join(Series).\
            where(Seasons.id == season_id).naive()[0]
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

    @staticmethod
    def refresh_not_found():
        not_found_chapters_per_season = SeriesManager._get_not_found_chapters_per_season()
        for serie in not_found_chapters_per_season:
            SeriesManager._refresh_not_found_by_serie(serie, not_found_chapters_per_season[serie])

    @staticmethod
    def _refresh_not_found_by_serie(serie_name, not_found_episodes_per_season):
        for season in not_found_episodes_per_season:
            season_uris = SeriesManager._get_uri_per_series_season(serie_name, season)
            for chapter in not_found_episodes_per_season[season]:
                if season_uris.get(chapter):
                    SeriesManager._update_chapter_uri(serie_name, season, chapter, season_uris.get(chapter))

    @staticmethod
    def _update_chapter_uri(serie_name, season_number, chapter_number, uri):
        chapter = Chapters.select().join(Seasons).join(Series).where(
            Seasons.season_number == season_number and
            Series.name == serie_name and
            Chapters.number == chapter_number
        )
        chapter[0].uri = uri
        chapter[0].status = 'READY TO DOWNLOAD'
        chapter[0].save()

    @staticmethod
    def _get_uri_per_series_season(serie_name, serie_season):
        return {chapter: torrent.magnet_link for chapter, torrent in
                TorrentSearcher().search_for_serie(serie_name, serie_season).iteritems()}

    @staticmethod
    def _get_not_found_chapters_per_season():
        not_found_chapters = Chapters.select(Chapters.number, Seasons.season_number, Series.name).\
            where(Chapters.status == 'NOT FOUND').join(Seasons).naive().join(Series).naive()
        chapters_per_serie = dict()
        for chapter in not_found_chapters:
            if not chapters_per_serie.get(chapter.name):
                chapters_per_serie[chapter.name] = {chapter.season_number: [chapter.number]}
            else:
                if not chapters_per_serie[chapter.name].get(chapter.season_number):
                    chapters_per_serie[chapter.name][chapter.season_number] = [chapter.number]
                else:
                    chapters_per_serie[chapter.name][chapter.season_number].append(chapter.number)
        return chapters_per_serie



#SeriesManager().refresh_not_found()
#SeriesManager()._update_chapter_uri("preacher", 2, 1, 'pepepe')
"""a = SeriesManager().add_series("preacher", 'c')
print a
b = SeriesManager().add_season(a, 2, 13)
print b
SeriesManager().add_chapters(b)"""

print SeriesManager().get_ready_to_download()