from model import *


def create_tables():
    ChapterStatus.create_table()
    Series.create_table()
    Seasons.create_table()
    Chapters.create_table()
    TorrentStatus.create_table()
    ActiveTorrents.create_table()


def insert_chapters_status():
    chapter_statuses = ['NOT FOUND', 'READY TO DOWNLOAD', 'DOWNLOADING', 'DOWNLOADED']
    for status in chapter_statuses:
        ChapterStatus.create(status_code=status)


def insert_torrent_status():
    torrent_status = ['STOPPED', 'DOWNLOADING', 'FINISHED']
    for status in torrent_status:
        TorrentStatus.create(status_code=status)


if __name__ == '__main__':

    create_tables()
    insert_chapters_status()
    insert_torrent_status()
