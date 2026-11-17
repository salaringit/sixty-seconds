from django.db.models.signals import post_save
from django.test import TestCase

from blog.models import Author, Post

from . import demo

N = 50


class BulkCreateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(name="A", email="a@example.com")

    def test_the_loop_runs_one_insert_per_object(self):
        with self.assertNumQueries(N):
            demo.bad(self.author, N)
        self.assertEqual(Post.objects.count(), N)

    def test_bulk_create_runs_one(self):
        with self.assertNumQueries(1):
            demo.good(self.author, N)
        self.assertEqual(Post.objects.count(), N)

    def test_batch_size_splits_the_insert(self):
        with self.assertNumQueries(5):
            demo.good(self.author, N, batch_size=10)

    def test_bulk_create_does_not_fire_post_save(self):
        fired = []

        def receiver(**kwargs):
            fired.append(1)

        # weak=False matters: Django holds receivers weakly by default, and a
        # local function would be collected before the signal ever fires.
        post_save.connect(receiver, sender=Post, weak=False)
        try:
            demo.bad(self.author, 3)
            self.assertEqual(len(fired), 3)

            fired.clear()
            demo.good(self.author, 3)
            self.assertEqual(fired, [])  # this is the trap
        finally:
            post_save.disconnect(receiver, sender=Post)
