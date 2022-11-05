from reviews.models import Comments  # , Reviews
from users.models import User
import csv


def run():
    with open('static/data/comments.csv') as file:
        reader = csv.reader(file)
        next(reader)

        Comments.objects.all().delete()

        for row in reader:
            print(row)

            # review, _ = Reviews.objects.get_or_create(id=row[1])
            author, _ = User.objects.get_or_create(id=row[3])

            comment = Comments(
                id=row[0],
                review_id=row[1],
                text=row[2],
                author=author,
                pub_date=row[4],
            )
            comment.save()
