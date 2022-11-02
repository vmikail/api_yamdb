from reviews.models import GenreTitle, Genre, Title
import csv


def run():
    with open('static/data/genre_title.csv') as file:
        reader = csv.reader(file)
        next(reader)

        GenreTitle.objects.all().delete()

        for row in reader:
            print(row)

            title, _ = Title.objects.get_or_create(id=row[1])
            genre, _ = Genre.objects.get_or_create(id=row[2])

            print(f'print1={title}')
            print(f'print2={genre}')

            genre_title = GenreTitle(
                id=row[0],
                title=title,
                genre=genre,
            )
            genre_title.save()
