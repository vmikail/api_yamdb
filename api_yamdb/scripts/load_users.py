from reviews.models import Reviews  # Title
from users.models import User
import csv


def run():
    with open('static/data/users.csv') as file:
        reader = csv.reader(file)
        next(reader)

        Reviews.objects.all().delete()

        for row in reader:
            print(row)

            # title_id, _ = Title.objects.get_or_create(id=row[1])
            # author, _ = User.objects.get_or_create(id=row[3])

            user = User(
                id=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6],
            )
            user.save()
