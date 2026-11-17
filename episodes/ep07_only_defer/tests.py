from django.test import TestCase

from blog.models import Author, Post

from . import demo

POSTS = 10


class OnlyDeferTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = Author.objects.create(name="A", email="a@example.com")
        for i in range(POSTS):
            Post.objects.create(
                author=author, title=f"Post {i}", body="x" * 5000
            )

    def test_only_selects_fewer_columns(self):
        sql = str(Post.objects.only("id", "title").query).lower()
        self.assertNotIn('"body"', sql)
        self.assertIn("title", sql)

    def test_touching_a_deferred_field_costs_a_query_per_object(self):
        with self.assertNumQueries(1):
            demo.only_what_you_render()

        with self.assertNumQueries(1 + POSTS):
            demo.the_only_trap()

    def test_defer_is_the_inverse(self):
        sql = str(Post.objects.defer("body").query).lower()
        self.assertNotIn('"body"', sql)

    def test_values_list_builds_no_model_instances(self):
        with self.assertNumQueries(1):
            titles = demo.no_instances_at_all()
        self.assertEqual(len(titles), POSTS)
        self.assertIsInstance(titles[0], str)  # a plain string, not a Post

    def test_every_route_returns_the_same_titles(self):
        self.assertEqual(
            sorted(demo.everything()), sorted(demo.no_instances_at_all())
        )
