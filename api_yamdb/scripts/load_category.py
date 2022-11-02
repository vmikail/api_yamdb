from reviews.models import Category
import csv


def run():
    with open('static/data/category.csv') as file:
        reader = csv.reader(file)
        next(reader)

        Category.objects.all().delete()

        for row in reader:
            print(row)

            # category, _ = Category.objects.get_or_create(name=row[-1])

            category = Category(
                id=row[0],
                name=row[1],
                slug=row[2],
            )
            category.save()
