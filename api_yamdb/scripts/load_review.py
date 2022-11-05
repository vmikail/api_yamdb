from reviews.models import Reviews  # , Title
from users.models import User
import csv


def run():
    with open('static/data/review.csv') as file:
        reader = csv.reader(file)
        next(reader)

        Reviews.objects.all().delete()

        for row in reader:
            print(row)

            # title_id, _ = Title.objects.get_or_create(id=row[1])
            author, _ = User.objects.get_or_create(id=row[3])
            print(f'title_id={row[1]}')

            review = Reviews(
                id=row[0],
                text=row[2],
                score=row[4],
                pub_date=row[5],
                author=author,
                title_id=row[1],
            )
            review.save()
