from django.test import TestCase

from blog.models import Author, Post

from . import demo

AUTHORS = 5


class AnnotateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(AUTHORS):
            author = Author.objects.create(
                name=f"Author {i}", email=f"a{i}@example.com"
            )
            for j in range(i):  # author i gets i posts
                Post.objects.create(
                    author=author, title=f"P{i}{j}", is_published=j % 2 == 0
                )

    def test_counting_in_python_runs_a_query_per_row(self):
        with self.assertNumQueries(1 + AUTHORS):
            demo.bad()

    def test_annotate_runs_one(self):
        with self.assertNumQueries(1):
            demo.good()

    def test_both_produce_the_same_numbers(self):
        self.assertEqual(sorted(demo.bad()), sorted(demo.good()))

    def test_you_can_filter_and_order_by_an_annotation(self):
        names = list(demo.prolific(minimum=2).values_list("name", flat=True))
        self.assertEqual(names, ["Author 4", "Author 3", "Author 2"])

    def test_count_with_a_filter_counts_a_subset_in_the_same_query(self):
        with self.assertNumQueries(1):
            by_name = {
                a.name: a.published_count for a in demo.published_only()
            }
        self.assertEqual(by_name["Author 4"], 2)  # j = 0 and 2
        self.assertEqual(by_name["Author 1"], 1)

    def test_aggregate_collapses_to_a_single_dict(self):
        self.assertEqual(demo.totals(), {"total": 10})
