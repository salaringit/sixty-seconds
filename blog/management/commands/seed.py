"""Demo data, so you can poke at the queries by hand instead of only through
the tests."""

import random

from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.models import Account, Author, Post, Tag


class Command(BaseCommand):
    help = "Populate the database with demo blog data"

    def add_arguments(self, parser):
        parser.add_argument("--authors", type=int, default=20)
        parser.add_argument("--posts", type=int, default=100)

    def handle(self, *args, **options):
        Post.objects.all().delete()
        Author.objects.all().delete()
        Tag.objects.all().delete()
        Account.objects.all().delete()

        tags = [Tag.objects.create(name=n) for n in
                ("django", "python", "sql", "performance", "testing")]

        authors = Author.objects.bulk_create([
            Author(name=f"Author {i}", email=f"author{i}@example.com")
            for i in range(options["authors"])
        ])
        authors = list(Author.objects.all())

        now = timezone.now()
        posts = Post.objects.bulk_create([
            Post(
                author=random.choice(authors),
                title=f"Post number {i}",
                body="lorem ipsum " * 400,
                views=random.randint(0, 5000),
                is_published=i % 3 != 0,
                published_at=now - timezone.timedelta(days=i),
            )
            for i in range(options["posts"])
        ])

        for post in Post.objects.all():
            post.tags.add(*random.sample(tags, k=random.randint(1, 3)))

        Account.objects.create(owner="salar", balance=1000)

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {Author.objects.count()} authors, "
            f"{Post.objects.count()} posts."
        ))
