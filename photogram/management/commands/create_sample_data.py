from django.core.management.base import BaseCommand
from accounts.models import User
from photogram.models import FollowRequest, Comment, Like, Photo
from faker import Faker
import random

class Command(BaseCommand):
    help = "Create random users"

    def handle(self, *args, **kwargs):
        faker = Faker()
        Faker.seed(1) # generate consistent sample data

        FollowRequest.objects.all().delete()
        Comment.objects.all().delete()
        Like.objects.all().delete()
        Photo.objects.all().delete()
        User.objects.all().delete()

        people = ["Alice", "Bob", "Carol", "Doug"]

        for person in people:
            user = User.objects.create(
                email=f"{person.lower()}@example.com",
                username=person.lower(),
                name=person,
                private=random.choice([True, False]),
                avatar_image=f"https://robohash.org/{person.lower()}"
            )
            user.set_password("password12321")
            user.save()

        users = User.objects.all()

        for first_user in users:
            for second_user in users:
                if random.random() < 0.75:
                    FollowRequest.objects.create(
                        sender=first_user,
                        recipient=second_user,
                        status=random.choice(["accepted", "rejected", "pending"])
                    )

        for user in users:
            for _ in range(random.randint(0, 30)):
                photo = Photo.objects.create(
                    caption=faker.text(),
                    owner=user,
                    image=f"https://robohash.org/{random.randint(1, 100)}"
                )

                for follower in user.followers():
                    if random.random() < 0.5:
                        Like.objects.create(photo=photo, fan=follower)

                    if random.random() < 0.25:
                        Comment.objects.create(
                            body=faker.text(),
                            photo=photo,
                            author=follower
                        )

        self.stdout.write(self.style.SUCCESS("Sample data created."))