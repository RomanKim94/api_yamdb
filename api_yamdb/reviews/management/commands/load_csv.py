from typing import OrderedDict
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import csv
from reviews.models import Category, Comment, Genre, Review, Title, User

USER_FILE_NAME = 'users.csv'
CATEGORY_FILE_NAME = 'category.csv'
GENRE_FILE_NAME = 'genre.csv'
TITLE_FILE_NAME = 'titles.csv'
TITLE_GENRE_FILE_NAME = 'genre_title.csv'
REVIEW_FILE_NAME = 'review.csv'
COMMENT_FILE_NAME = 'comments.csv'
FILES_MODELS = OrderedDict((
    (USER_FILE_NAME, User),
    (CATEGORY_FILE_NAME, Category),
    (GENRE_FILE_NAME, Genre),
    (TITLE_FILE_NAME, Title),
    (TITLE_GENRE_FILE_NAME, Title.genre.through),
    (REVIEW_FILE_NAME, Review),
    (COMMENT_FILE_NAME, Comment),
))
DEFAULT_CSV_FOLDER_PATH = os.path.join(settings.BASE_DIR, 'static', 'data')
FILE_NOT_EXIST_ERROR = 'Файла {file} не существует'
FILE_NOT_CSV_ERROR = 'Файл {file} не соответствует расширению csv'
UNEXPECTED_FILE_NAME_ERROR = 'Неизвестный файл {file}'
SUCCESS_MODEL_LOAD = 'Успешно загружено {count} записей в {model}.'


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            nargs='*',
            type=str,
            help='Путь от корня проекта до csv файла.'
        )

    def validate_file_path(self, file_path):
        if not os.path.isfile(file_path):
            raise CommandError(
                FILE_NOT_EXIST_ERROR.format(file=file_path)
            )
        if not file_path.endswith('.csv'):
            raise CommandError(
                FILE_NOT_CSV_ERROR.format(file=file_path)
            )
        return file_path

    def get_default_csv_files(self):
        return [
            self.validate_file_path(
                os.path.join(DEFAULT_CSV_FOLDER_PATH, file)
            ) for file in FILES_MODELS.keys()
        ]

    def get_csv_files(self, file_path):
        if not file_path:
            return self.get_default_csv_files()
        return [
            self.validate_file_path(
                os.path.join(DEFAULT_CSV_FOLDER_PATH, path)
            ) for path in file_path
        ]

    def get_model_objects(self, model, file_data):
        related_fields = []
        m_to_m_fields = []
        objects = []
        for field in model._meta.fields:
            if field.is_relation:
                if field.many_to_many:
                    m_to_m_fields.append(field.name)
                else:
                    related_fields.append(field.name)
        for row in file_data:
            related_row = row.copy()
            for row_field in row.keys():
                if (
                    row_field in related_fields
                    and row_field not in m_to_m_fields
                ):
                    related_row[row_field], _ = model._meta.get_field(
                        row_field
                    ).related_model.objects.get_or_create(pk=row[row_field])
            objects.append(model(**related_row))
        return objects

    def get_model(self, csv_file_path):
        model = FILES_MODELS.get(csv_file_path.split(os.sep)[-1])
        if not model:
            raise CommandError(
                UNEXPECTED_FILE_NAME_ERROR.format(
                    file=csv_file_path.split(os.sep)[-1]
                )
            )
        return model

    def get_objects_from_csv_file(self, csv_file_path, model):
        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            if csv_file_path.endswith(TITLE_GENRE_FILE_NAME):
                return [model(**row) for row in reader]
            return self.get_model_objects(model, reader)

    def handle(self, *args, **options):
        csv_files = self.get_csv_files(options.get('file_path'))
        for file_path in csv_files:
            model = self.get_model(file_path)
            model.objects.all().delete()
            objects = self.get_objects_from_csv_file(file_path, model)
            model.objects.bulk_create(objects)
            self.stdout.write(
                SUCCESS_MODEL_LOAD.format(
                    count=len(objects),
                    model=model.__name__,
                )
            )
