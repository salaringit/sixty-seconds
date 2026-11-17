from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext

from blog.models import Author, Post

from . import demo


class ExistsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = Author.objects.create(name="A", email="a@example.com")
        for i in range(5):
            Post.objects.create(author=author, title=f"P{i}", is_published=True)

    def test_count_asks_the_database_to_count_everything(self):
        with CaptureQueriesContext(connection) as ctx:
            demo.bad()
        self.assertIn("COUNT", ctx.captured_queries[0]["sql"].upper())

    def test_exists_stops_at_the_first_row(self):
        with CaptureQueriesContext(connection) as ctx:
            demo.good()
        sql = ctx.captured_queries[0]["sql"].upper()
        self.assertIn("LIMIT 1", sql)
        self.assertNotIn("COUNT", sql)

    def test_both_answer_the_same_question(self):
        self.assertEqual(demo.bad(), demo.good())

    def test_checking_first_then_fetching_runs_two_queries(self):
        with self.assertNumQueries(2):
            demo.wasteful()

    def test_evaluating_once_runs_one(self):
        with self.assertNumQueries(1):
            demo.efficient()

    def test_both_routes_return_the_same_rows(self):
        self.assertEqual(
            [p.pk for p in demo.wasteful()], [p.pk for p in demo.efficient()]
        )

    def test_exists_and_count_are_free_on_an_evaluated_queryset(self):
        """The widely repeated claim that .exists() fires an extra query on an
        evaluated queryset is false: Django checks _result_cache first."""
        posts = Post.objects.filter(is_published=True)
        list(posts)

        with self.assertNumQueries(0):
            exists, count, truthy = demo.already_evaluated(posts)

        self.assertEqual((exists, count, truthy), (True, 5, True))
