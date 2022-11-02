from reviews.models import Genre
import csv


def run():
    with open('static/data/genre.csv') as file:
        reader = csv.reader(file)
        next(reader)

        Genre.objects.all().delete()

        for row in reader:
            print(row)

            # category, _ = Genre.objects.get_or_create(id=row[3])

            genre = Genre(
                id=row[0],
                name=row[1],
                slug=row[2],
            )
            genre.save()
