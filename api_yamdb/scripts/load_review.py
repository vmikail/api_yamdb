from reviews.models import Reviews, Title, User
import csv


def run():
    with open('static/data/review.csv') as file:
        reader = csv.reader(file)
        next(reader)

        Reviews.objects.all().delete()

        for row in reader:
            print(row)

            title_id, _ = Title.objects.get_or_create(id=row[4])
            author, _ = User.objects.get_or_create(id=row[5])

            review = Reviews(
                id=row[0],
                title_id=title_id,
                text=row[1],
                score=row[2],
                pub_date=row[3],
            )
            review.save()
