from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from blog.models import Author, Post, PostQuerySet

from . import demo


class CustomQuerySetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.me = Author.objects.create(name="me", email="me@example.com")
        other = Author.objects.create(name="other", email="o@example.com")
        now = timezone.now()

        cls.newer = Post.objects.create(
            author=cls.me, title="newer", is_published=True,
            published_at=now - timedelta(days=1),
        )
        cls.older = Post.objects.create(
            author=cls.me, title="older", is_published=True,
            published_at=now - timedelta(days=5),
        )
        Post.objects.create(
            author=cls.me, title="scheduled", is_published=True,
            published_at=now + timedelta(days=1),      # not published yet
        )
        Post.objects.create(
            author=cls.me, title="draft", is_published=False, published_at=now
        )
        Post.objects.create(
            author=other, title="someone else", is_published=True,
            published_at=now,
        )

    def test_the_chain_returns_the_same_thing_as_the_hand_written_filter(self):
        self.assertEqual(
            list(demo.before(self.me)), list(demo.after(self.me))
        )

    def test_it_is_still_one_query(self):
        with self.assertNumQueries(1):
            list(demo.after(self.me))

    def test_scheduled_and_draft_posts_are_excluded(self):
        titles = list(demo.after(self.me).values_list("title", flat=True))
        self.assertEqual(titles, ["newer", "older"])

    def test_every_method_returns_a_queryset_which_is_why_they_chain(self):
        self.assertIsInstance(Post.objects.published(), PostQuerySet)
        self.assertIsInstance(Post.objects.published().by(self.me), PostQuerySet)
