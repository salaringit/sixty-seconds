# EP08 — Stop counting in Python

**The problem**
`author.posts.count()` inside a loop is one COUNT query per row.

**The fix**
`annotate(post_count=Count("posts"))` — one statement, a GROUP BY with a COUNT.

**The part tutorials skip**
The annotation is a real database column, so you can filter and order by it. `annotate` gives a value per row; `aggregate` collapses to one dict. `Count(..., filter=Q(...))` counts a subset without a second query.

## Files

| File | What's in it |
|---|---|
| `demo.py` | the slow version and the fast version, side by side |
| `tests.py` | the proof — query counts asserted with `assertNumQueries` |

## Run it

```bash
python manage.py test episodes.ep08_annotate
```
