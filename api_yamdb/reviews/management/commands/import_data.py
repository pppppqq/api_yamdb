import csv
import os

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction

from reviews.models import Category, Comment, Genre, Review, Title, User


def import_users(file_path):
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            User.objects.get_or_create(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'] or '',
                first_name=row['first_name'] or '',
                last_name=row['last_name'] or ''
            )


def import_categories(file_path):
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            Category.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )


def import_genres(file_path):
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            Genre.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )


def import_titles(file_path):
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = Category.objects.get(id=row['category'])
            Title.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=category
            )


def import_reviews(file_path):
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            author = User.objects.get(id=row['author'])
            title = Title.objects.get(id=row['title_id'])
            Review.objects.get_or_create(
                id=row['id'],
                title=title,
                text=row['text'],
                author=author,
                score=row['score'],
                pub_date=row['pub_date']
            )


def import_comments(file_path):
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            author = User.objects.get(id=row['author'])
            review = Review.objects.get(id=row['review_id'])
            Comment.objects.get_or_create(
                id=row['id'],
                review=review,
                text=row['text'],
                author=author,
                created=row['pub_date']
            )


def import_genre_title(file_path):
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = Title.objects.get(id=row['title_id'])
            genre = Genre.objects.get(id=row['genre_id'])
            title.genre.add(genre)


class Command(BaseCommand):
    help = 'Импортирует данные из CSV-файлов в базу данных'

    def handle(self, *args, **options):
        data_path = os.path.join(settings.BASE_DIR, 'static', 'data')

        try:
            with transaction.atomic():
                self.stdout.write('Импорт пользователей...')
                import_users(os.path.join(data_path, 'users.csv'))

                self.stdout.write('Импорт категорий...')
                import_categories(os.path.join(data_path, 'category.csv'))

                self.stdout.write('Импорт жанров...')
                import_genres(os.path.join(data_path, 'genre.csv'))

                self.stdout.write('Импорт произведений...')
                import_titles(os.path.join(data_path, 'titles.csv'))

                self.stdout.write('Импорт связей жанров...')
                import_genre_title(os.path.join(data_path, 'genre_title.csv'))

                self.stdout.write('Импорт отзывов...')
                import_reviews(os.path.join(data_path, 'review.csv'))

                self.stdout.write('Импорт комментариев...')
                import_comments(os.path.join(data_path, 'comments.csv'))

            self.stdout.write(
                self.style.SUCCESS('Все данные успешно импортированы!')
            )

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Ошибка при импорте: {e}'))
