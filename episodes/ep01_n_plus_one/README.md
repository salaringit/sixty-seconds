# EP01 — Your loop is running 101 queries

**The problem**
`Post.objects.all()` then touching `post.author` fetches the author once per post.

**The fix**
`select_related("author")` — one SQL JOIN, one query.

**The part tutorials skip**
`select_related` only works on forward ForeignKey and OneToOne. For ManyToMany or reverse relations it does nothing — use `prefetch_related`, which runs two queries and joins them in Python.

## Files

| File | What's in it |
|---|---|
| `demo.py` | the slow version and the fast version, side by side |
| `tests.py` | the proof — query counts asserted with `assertNumQueries` |

## Run it

```bash
python manage.py test episodes.ep01_n_plus_one
```
