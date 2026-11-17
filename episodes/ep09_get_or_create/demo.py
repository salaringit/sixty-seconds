"""EP09 — get_or_create is a SELECT followed by an INSERT, with a race window
in between."""

from blog.models import Author


def get_or_create(email, name="new"):
    """Safe only because Author.Meta declares a UniqueConstraint on email.
    Without it, two concurrent requests both miss the SELECT and both INSERT."""
    return Author.objects.get_or_create(
        email=email, defaults={"name": name}
    )


def create_duplicate(email, name="dup"):
    """What the database does when the constraint catches a second insert:
    raises IntegrityError. That is the protection working."""
    return Author.objects.create(email=email, name=name)
