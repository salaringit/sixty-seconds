from django.test import TestCase

from blog.models import Author, Post

from . import demo


class FExpressionTests(TestCase):
    def setUp(self):
        author = Author.objects.create(name="A", email="a@example.com")
        self.post = Post.objects.create(author=author, title="P", views=0)

    def test_read_modify_write_loses_an_increment(self):
        """Two requests that both read before either writes. No threads
        needed — this is the race, made deterministic."""
        request_a = Post.objects.get(pk=self.post.pk)
        request_b = Post.objects.get(pk=self.post.pk)  # both read 0

        demo.bad(request_a)
        demo.bad(request_b)

        self.post.refresh_from_db()
        self.assertEqual(self.post.views, 1)  # two clicks, one view recorded

    def test_f_expression_keeps_both(self):
        demo.good(self.post.pk)
        demo.good(self.post.pk)

        self.post.refresh_from_db()
        self.assertEqual(self.post.views, 2)

    def test_f_expression_is_one_query_instead_of_two(self):
        post = Post.objects.get(pk=self.post.pk)
        with self.assertNumQueries(1):  # the SELECT already happened above
            demo.bad(post)
        with self.assertNumQueries(1):  # SELECT and UPDATE in one statement
            demo.good(self.post.pk)

    def test_the_instance_in_memory_is_stale_after_an_f_update(self):
        demo.good(self.post.pk)
        self.assertEqual(self.post.views, 0)  # still the old value
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, 1)
