from model import *


def create_tables():
    ChapterStatus.create_table()
    Series.create_table()
    Seasons.create_table()
    Chapters.create_table()


def insert_chapters_status():
    chapter_statuses = ['NOT FOUND', 'READY TO DOWNLOAD', 'DOWNLOADED']
    for status in chapter_statuses:
        ChapterStatus.create(status_name=status)


if __name__ == '__main__':

    create_tables()
    insert_chapters_status()
