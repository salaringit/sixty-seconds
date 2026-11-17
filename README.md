# sixty-seconds

Runnable code from **[Mainloop](https://youtube.com/@mainlooop)** — one real
engineering idea per video, in sixty seconds.

Every snippet you see on screen lives here, in a Django project you can actually
run. Nothing in the videos is pseudo-code.

## Season 1 — 60 Seconds with Django

| # | Episode | The idea | Folder |
|---|---|---|---|
| 01 | Your loop is running 101 queries | N+1, `select_related` vs `prefetch_related` | [`01-n-plus-one`](01-n-plus-one) |
| 02 | `.count() > 0` is a bug | `.exists()` vs `.count()` vs truthiness | [`02-exists`](02-exists) |
| 03 | 1000 saves vs 1 query | `bulk_create` and its three traps | [`03-bulk-create`](03-bulk-create) |
| 04 | This code silently loses data | `F()` expressions, race conditions | [`04-f-expressions`](04-f-expressions) |
| 05 | Corrupt data halfway through | `transaction.atomic` | [`05-atomic`](05-atomic) |
| 06 | How do you write OR? | `Q` objects | [`06-q-objects`](06-q-objects) |
| 07 | Loading 40 columns to show 2 | `only` / `defer` / `values_list` | [`07-only-defer`](07-only-defer) |
| 08 | Stop counting in Python | `annotate` vs `aggregate` | [`08-annotate`](08-annotate) |
| 09 | `get_or_create` makes duplicates | `UniqueConstraint` | [`09-get-or-create`](09-get-or-create) |
| 10 | Delete your fat views | custom `QuerySet.as_manager()` | [`10-custom-queryset`](10-custom-queryset) |

## Running it

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
python manage.py migrate
python manage.py seed           # generates the demo data the episodes query
python manage.py test
```

SQLite by default, so there's nothing to install. A few episodes behave
differently on PostgreSQL (`bulk_create` returning primary keys, for one) — those
are called out in the episode's own README.

## How each episode folder is laid out

```
NN-slug/
  README.md      the idea, the before/after, and the gotcha the video skips
  demo.py        the bad version and the good version, side by side
  test_demo.py   asserts the query counts, so the claim in the video is proven
```

The tests are the point. When an episode says "101 queries become 1", there's an
`assertNumQueries(1)` behind it.

## License

MIT. Use anything here in your own work.
