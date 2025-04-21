import csv
import os

import django
from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()

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
                bio=row['bio'] or None,
                first_name=row['first_name'] or None,
                last_name=row['last_name'] or None
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
                pub_date=row['pub_date']
            )


def import_genre_title(file_path):
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = Title.objects.get(id=row['title_id'])
            genre = Genre.objects.get(id=row['genre_id'])
            title.genre.add(genre)


def main():
    data_path = 'api_yamdb/static/data/'

    try:
        with transaction.atomic():
            print("Импорт пользователей...")
            import_users(os.path.join(data_path, 'users.csv'))

            print("Импорт категорий...")
            import_categories(os.path.join(data_path, 'category.csv'))

            print("Импорт жанров...")
            import_genres(os.path.join(data_path, 'genre.csv'))

            print("Импорт произведений...")
            import_titles(os.path.join(data_path, 'titles.csv'))

            print("Импорт связей жанров...")
            import_genre_title(os.path.join(data_path, 'genre_title.csv'))

            print("Импорт отзывов...")
            import_reviews(os.path.join(data_path, 'review.csv'))

            print("Импорт комментариев...")
            import_comments(os.path.join(data_path, 'comments.csv'))

        print("Все данные успешно импортированы!")

    except Exception as e:
        print(f"Ошибка при импорте: {str(e)}")


if __name__ == '__main__':
    main()
