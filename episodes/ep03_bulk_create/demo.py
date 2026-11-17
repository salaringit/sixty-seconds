"""EP03 — a loop of .create() is one INSERT and one round trip each."""

from blog.models import Post


def bad(author, n):
    for i in range(n):
        Post.objects.create(author=author, title=f"Post {i}")


def good(author, n, batch_size=500):
    """One multi-row INSERT per batch.

    Three things it does NOT do:
      * call save()
      * fire pre_save / post_save
      * set primary keys on the returned objects (PostgreSQL excepted)
    """
    return Post.objects.bulk_create(
        [Post(author=author, title=f"Post {i}") for i in range(n)],
        batch_size=batch_size,
    )
