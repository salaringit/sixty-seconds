"""EP08 — counting in Python costs one query per row."""

from django.db.models import Count, Q

from blog.models import Author, Post


def bad():
    """author.posts.count() inside a loop: one COUNT per author."""
    return [(a.name, a.posts.count()) for a in Author.objects.all()]


def good():
    """One statement: a GROUP BY with a COUNT, attached to every row."""
    authors = Author.objects.annotate(post_count=Count("posts"))
    return [(a.name, a.post_count) for a in authors]


def prolific(minimum=2):
    """Because the annotation is a real database column, you can filter and
    order by it. You cannot do that with a Python loop."""
    return (
        Author.objects.annotate(post_count=Count("posts"))
        .filter(post_count__gte=minimum)
        .order_by("-post_count")
    )


def published_only():
    """Counting a subset without a second query."""
    return Author.objects.annotate(
        published_count=Count("posts", filter=Q(posts__is_published=True))
    )


def totals():
    """annotate = a value per row. aggregate = one dict for the whole
    queryset."""
    return Post.objects.aggregate(total=Count("id"))
