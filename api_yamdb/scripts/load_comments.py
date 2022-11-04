from reviews.models import Comments, Reviews, User
import csv


def run():
    with open('static/data/review.csv') as file:
        reader = csv.reader(file)
        next(reader)

        Comments.objects.all().delete()

        for row in reader:
            print(row)

            review, _ = Reviews.objects.get_or_create(id=row[3])
            author, _ =User.objects.get_or_create(id=row[4])

            comment = Comments(
                id=row[0],
                review_id=review,
                text=row[1],
                author=author,
                pub_date=row[2],
            )
            comment.save()
