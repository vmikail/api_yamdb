from reviews.models import Title, Category
import csv


def run():
    with open('static/data/titles.csv') as file:
        reader = csv.reader(file)
        next(reader)

        Title.objects.all().delete()

        for row in reader:
            print(row)

            category, _ = Category.objects.get_or_create(id=row[3])

            title = Title(
                id=row[0],
                name=row[1],
                year=row[2],
                category=category
            )
            title.save()
