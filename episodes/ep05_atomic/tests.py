from decimal import Decimal

from django.test import TransactionTestCase

from blog.models import Account, Order

from . import demo


class AtomicTests(TransactionTestCase):
    """TransactionTestCase, not TestCase: TestCase wraps every test in a
    transaction of its own, which would hide the very thing being tested."""

    def setUp(self):
        self.account = Account.objects.create(
            owner="salar", balance=Decimal("100.00")
        )

    def test_without_atomic_the_money_is_gone_and_there_is_no_order(self):
        with self.assertRaises(demo.CheckoutFailed):
            demo.bad(self.account, "30.00")

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("70.00"))  # charged
        self.assertEqual(Order.objects.count(), 0)                # no order

    def test_atomic_rolls_the_whole_thing_back(self):
        with self.assertRaises(demo.CheckoutFailed):
            demo.good(self.account, "30.00")

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("100.00"))  # untouched
        self.assertEqual(Order.objects.count(), 0)

    def test_the_happy_path_still_commits(self):
        demo.good(self.account, "30.00", fail=False)

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("70.00"))
        self.assertEqual(Order.objects.count(), 1)
