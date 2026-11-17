"""EP05 — Django autocommits every query, so a view can stop halfway and
leave the database inconsistent."""

from decimal import Decimal

from django.db import transaction

from blog.models import Account, Order


class CheckoutFailed(Exception):
    pass


def bad(account, price, fail=True):
    """The balance change commits on its own. When the next line raises, the
    money is gone and there is no order."""
    account.balance -= Decimal(price)
    account.save()

    if fail:
        raise CheckoutFailed("payment provider rejected the order")

    Order.objects.create(account=account, total=price)


def good(account, price, fail=True):
    """All of it, or none of it.

    Two rules: catch the exception OUTSIDE the block, and never make network
    calls inside it — you would be holding database locks open."""
    with transaction.atomic():
        account.balance -= Decimal(price)
        account.save()

        if fail:
            raise CheckoutFailed("payment provider rejected the order")

        Order.objects.create(account=account, total=price)
