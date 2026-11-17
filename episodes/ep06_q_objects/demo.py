"""EP06 — there is no keyword syntax for OR. Q objects are the only way."""

from django.db.models import Q

from blog.models import Post


def implicit_and(author):
    """Two kwargs in one filter is AND. So is chaining .filter()."""
    return Post.objects.filter(is_published=True, author=author)


def either(author):
    """| is OR, & is AND, ~ is NOT."""
    return Post.objects.filter(Q(is_published=True) | Q(author=author))


def not_published():
    return Post.objects.filter(~Q(is_published=True))


def search(terms, published_only=True):
    """How a real search filter gets built: start from an empty Q and OR
    conditions onto it.

    Q arguments must come before keyword arguments in the same filter() call,
    or Python raises a SyntaxError."""
    query = Q()
    for term in terms:
        query |= Q(title__icontains=term)

    if published_only:
        return Post.objects.filter(query, is_published=True)
    return Post.objects.filter(query)
