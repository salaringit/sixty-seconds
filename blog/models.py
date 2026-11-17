from django.db import models
from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()

    class Meta:
        # EP09: this constraint is what actually makes get_or_create safe.
        constraints = [
            models.UniqueConstraint(fields=["email"], name="unique_author_email")
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name


class PostQuerySet(models.QuerySet):
    """EP10: the business rules live here, once, instead of being re-typed in
    every view, task and admin action. Every method returns a queryset, so they
    chain."""

    def published(self):
        return self.filter(is_published=True, published_at__lte=timezone.now())

    def by(self, author):
        return self.filter(author=author)

    def recent(self):
        return self.order_by("-published_at")


class Post(models.Model):
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=200)
    body = models.TextField(default="")
    views = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)

    objects = PostQuerySet.as_manager()

    def __str__(self):
        return self.title


class Account(models.Model):
    """EP05: the two models that make a half-finished checkout visible."""

    owner = models.CharField(max_length=120)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Order(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="orders"
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)
