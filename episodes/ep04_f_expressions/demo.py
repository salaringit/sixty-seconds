"""EP04 — read-modify-write is a race condition."""

from django.db.models import F

from blog.models import Post


def bad(post):
    """Reads the value into Python, adds one there, writes it back. Two
    requests that read the same value both write the same value, and one
    increment disappears."""
    post.views = post.views + 1
    post.save()


def good(pk):
    """SET views = views + 1 — the database does the arithmetic, atomically.

    Note the instance in memory is stale afterwards: refresh_from_db() if you
    need the new number."""
    Post.objects.filter(pk=pk).update(views=F("views") + 1)
