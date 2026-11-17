"""EP01 — N+1: one loop, a hundred and one queries."""

from blog.models import Post


def bad():
    """1 query for the posts, then +1 for every single author access."""
    return [f"{p.title} by {p.author.name}" for p in Post.objects.all()]


def good():
    """select_related does a SQL JOIN: one query, same data.

    Only works for forward ForeignKey and OneToOne — anything that is a single
    row on the other side."""
    return [
        f"{p.title} by {p.author.name}"
        for p in Post.objects.select_related("author")
    ]


def bad_many():
    """Same bug, multi-valued relation. select_related cannot help here."""
    return [[t.name for t in p.tags.all()] for p in Post.objects.all()]


def good_many():
    """prefetch_related: two queries (posts, then tags), joined in Python."""
    return [
        [t.name for t in p.tags.all()]
        for p in Post.objects.prefetch_related("tags")
    ]
