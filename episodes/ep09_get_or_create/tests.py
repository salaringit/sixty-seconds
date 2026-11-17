from django.db import IntegrityError, connection, transaction
from django.test import TestCase
from django.test.utils import CaptureQueriesContext

from blog.models import Author

from . import demo


class GetOrCreateTests(TestCase):
    def test_first_call_creates_second_call_gets(self):
        author, created = demo.get_or_create("a@example.com", name="first")
        self.assertTrue(created)

        again, created = demo.get_or_create("a@example.com", name="second")
        self.assertFalse(created)
        self.assertEqual(again.pk, author.pk)
        self.assertEqual(again.name, "first")  # defaults are ignored on a get

    def test_it_is_a_select_then_an_insert_which_is_where_the_race_lives(self):
        with CaptureQueriesContext(connection) as ctx:
            demo.get_or_create("b@example.com")

        statements = [q["sql"].split()[0].upper() for q in ctx.captured_queries]
        # SELECT, SAVEPOINT, INSERT, RELEASE - get_or_create guards the insert
        # with a savepoint so a failure does not poison the transaction.
        self.assertEqual(statements[0], "SELECT")
        self.assertIn("INSERT", statements)

        with self.assertNumQueries(1):  # second time: SELECT only, no insert
            demo.get_or_create("b@example.com")

    def test_the_constraint_is_what_actually_stops_duplicates(self):
        demo.get_or_create("c@example.com")

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                demo.create_duplicate("c@example.com")

        self.assertEqual(Author.objects.filter(email="c@example.com").count(), 1)

    def test_the_constraint_is_declared_on_the_model(self):
        names = [c.name for c in Author._meta.constraints]
        self.assertIn("unique_author_email", names)
