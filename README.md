# sixty-seconds

Runnable code from **[Mainloop](https://youtube.com/@mainlooop)** — one real
engineering idea per video, in sixty seconds.

Every snippet you see on screen lives here, in a Django project you can actually
run. Nothing in the videos is pseudo-code.

## Season 1 — 60 Seconds with Django

| # | Episode | The idea | Folder |
|---|---|---|---|
| 01 | Your loop is running 101 queries | N+1, `select_related` vs `prefetch_related` | [`ep01_n_plus_one`](episodes/ep01_n_plus_one) |
| 02 | `.count() > 0` is a bug | `.exists()` vs `.count()` vs truthiness | [`ep02_exists`](episodes/ep02_exists) |
| 03 | 1000 saves vs 1 query | `bulk_create` and its three traps | [`ep03_bulk_create`](episodes/ep03_bulk_create) |
| 04 | This code silently loses data | `F()` expressions, race conditions | [`ep04_f_expressions`](episodes/ep04_f_expressions) |
| 05 | Corrupt data halfway through | `transaction.atomic` | [`ep05_atomic`](episodes/ep05_atomic) |
| 06 | How do you write OR? | `Q` objects | [`ep06_q_objects`](episodes/ep06_q_objects) |
| 07 | Loading 40 columns to show 2 | `only` / `defer` / `values_list` | [`ep07_only_defer`](episodes/ep07_only_defer) |
| 08 | Stop counting in Python | `annotate` vs `aggregate` | [`ep08_annotate`](episodes/ep08_annotate) |
| 09 | `get_or_create` makes duplicates | `UniqueConstraint` | [`ep09_get_or_create`](episodes/ep09_get_or_create) |
| 10 | Delete your fat views | custom `QuerySet.as_manager()` | [`ep10_custom_queryset`](episodes/ep10_custom_queryset) |

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
episodes/epNN_slug/
  README.md   the idea, the before/after, and the gotcha the video skips
  demo.py     the slow version and the fast version, side by side
  tests.py    the proof — query counts asserted with assertNumQueries
```

The tests are the point. When an episode says "101 queries become 1", there is an
`assertNumQueries(1)` behind it.

Writing them has already changed an episode: EP02 originally repeated the common
claim that `.exists()` costs an extra query on an already-evaluated queryset. It
doesn't — Django reads the result cache first. The test caught it before the
video was recorded.

## License

MIT. Use anything here in your own work.
