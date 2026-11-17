"""EP10 — the same filter chain, copy-pasted into four files, is four
definitions of the same business rule.

The queryset itself lives in blog/models.py as PostQuerySet, attached with
PostQuerySet.as_manager(). This file shows the before and the after.
"""

from django.utils import timezone

from blog.models import Post


def before(author):
    """What this looks like in views.py, api.py, tasks.py and admin.py — and
    what gets edited in only three of them, six months from now."""
    return Post.objects.filter(
        is_published=True,
        published_at__lte=timezone.now(),
        author=author,
    ).order_by("-published_at")


def after(author):
    """One line. The definition of 'published' lives in exactly one place.

    These chain because every method returns a queryset — which is precisely
    what Manager methods cannot do."""
    return Post.objects.published().by(author).recent()
