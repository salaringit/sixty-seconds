"""EP07 — objects.all() is SELECT *, plus the cost of building a full model
instance for every row."""

from blog.models import Post


def everything():
    return [p.title for p in Post.objects.all()]


def only_what_you_render():
    """SELECT id, title. Still model instances — touch any other field and
    Django silently re-queries, once per object."""
    return [p.title for p in Post.objects.only("id", "title")]


def the_only_trap():
    """Deliberately touching a deferred field, to show the cost."""
    return [p.body for p in Post.objects.only("id", "title")]


def defer_the_blob():
    """The inverse: load everything except the heavy column."""
    return [p.title for p in Post.objects.defer("body")]


def no_instances_at_all():
    """No model construction. The right tool for dropdowns, exports, ID
    lists — anything you are not going to call methods on."""
    return list(Post.objects.values_list("title", flat=True))
