from django.test import TestCase

from blog.models import Author, Post, Tag

from . import demo

POSTS = 10


class NPlusOneTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        tag = Tag.objects.create(name="django")
        for i in range(POSTS):
            author = Author.objects.create(
                name=f"Author {i}", email=f"a{i}@example.com"
            )
            post = Post.objects.create(author=author, title=f"Post {i}")
            post.tags.add(tag)

    def test_bad_runs_one_query_per_post(self):
        with self.assertNumQueries(1 + POSTS):
            demo.bad()

    def test_select_related_collapses_it_to_one(self):
        with self.assertNumQueries(1):
            demo.good()

    def test_both_return_the_same_data(self):
        self.assertEqual(demo.bad(), demo.good())

    def test_many_to_many_needs_prefetch_not_select_related(self):
        with self.assertNumQueries(1 + POSTS):
            demo.bad_many()
        with self.assertNumQueries(2):
            demo.good_many()
