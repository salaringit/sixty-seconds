"""EP02 — .count() > 0 asks the database to count every matching row to
answer a yes/no question."""

from blog.models import Post


def bad():
    """SELECT COUNT(*) — counts every match just to compare against zero."""
    return Post.objects.filter(is_published=True).count() > 0


def good():
    """SELECT 1 ... LIMIT 1 — stops at the first hit."""
    return Post.objects.filter(is_published=True).exists()


def wasteful():
    """The real trap, and it is not what most articles claim.

    This checks, and then builds a *second* queryset to fetch the same rows.
    Two separate querysets means two separate queries."""
    if Post.objects.filter(is_published=True).exists():
        return list(Post.objects.filter(is_published=True))
    return []


def efficient():
    """If you need the rows anyway, do not ask first. Evaluate once and use
    the truthiness of what you got back."""
    posts = list(Post.objects.filter(is_published=True))
    if posts:
        return posts
    return []


def already_evaluated(posts):
    """Worth knowing: on an evaluated queryset, .exists() and .count() both
    read the result cache and cost nothing. Django checks _result_cache before
    it touches the database."""
    return posts.exists(), posts.count(), bool(posts)
