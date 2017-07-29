import peewee
import os

path = os.path.dirname(os.path.abspath(__file__))
database = peewee.SqliteDatabase(os.path.join(path, 'database.db'))


class Series(peewee.Model):
    series_id = peewee.BigIntegerField(primary_key=True)
    name = peewee.CharField(unique=True)
    download_path = peewee.CharField()

    class Meta:
        database = database


class Seasons(peewee.Model):

    season_id = peewee.BigIntegerField(primary_key=True)
    series_id = peewee.ForeignKeyField(Series)
    season_number = peewee.BigIntegerField()
    chapters = peewee.BigIntegerField()

    class Meta:
        database = database


class ChapterStatus(peewee.Model):

    status_name = peewee.CharField(primary_key=True)

    class Meta:
        database = database


class Chapters(peewee.Model):

    chapter_id = peewee.BigIntegerField(primary_key=True)
    number = peewee.BigIntegerField()
    season_id = peewee.ForeignKeyField(Seasons)
    has_subtitles = peewee.BooleanField(default=False)
    status = peewee.ForeignKeyField(ChapterStatus)
    uri = peewee.CharField(null=True)

    class Meta:
        database = database
