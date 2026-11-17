from django.test import TestCase

from blog.models import Author, Post

from . import demo


class QObjectTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.me = Author.objects.create(name="me", email="me@example.com")
        cls.other = Author.objects.create(name="other", email="o@example.com")

        Post.objects.create(author=cls.me, title="Django drafts", is_published=False)
        Post.objects.create(author=cls.other, title="Published post", is_published=True)
        Post.objects.create(author=cls.other, title="Postgres notes", is_published=False)

    def test_two_kwargs_mean_and(self):
        sql = str(demo.implicit_and(self.me).query).upper()
        self.assertIn(" AND ", sql)
        self.assertNotIn(" OR ", sql)
        self.assertEqual(demo.implicit_and(self.me).count(), 0)

    def test_the_pipe_means_or(self):
        sql = str(demo.either(self.me).query).upper()
        self.assertIn(" OR ", sql)
        # the published one, plus both of mine
        self.assertEqual(demo.either(self.me).count(), 2)

    def test_tilde_means_not(self):
        self.assertEqual(demo.not_published().count(), 2)

    def test_a_dynamic_search_ors_the_terms_together(self):
        found = demo.search(["django", "postgres"], published_only=False)
        self.assertEqual(
            sorted(found.values_list("title", flat=True)),
            ["Django drafts", "Postgres notes"],
        )

    def test_q_args_combine_with_kwargs_as_and(self):
        self.assertEqual(demo.search(["post"], published_only=True).count(), 1)
