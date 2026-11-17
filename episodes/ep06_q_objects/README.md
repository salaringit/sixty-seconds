# EP06 — How do you write OR?

**The problem**
`filter(a=1, b=2)` is AND. Chained `.filter()` is AND. There is no keyword syntax for OR.

**The fix**
`Q` objects: `|` is OR, `&` is AND, `~` is NOT.

**The part tutorials skip**
`Q` arguments must come before keyword arguments in the same `filter()` call. Start from an empty `Q()` and `|=` in a loop to build a dynamic search filter.

## Files

| File | What's in it |
|---|---|
| `demo.py` | the slow version and the fast version, side by side |
| `tests.py` | the proof — query counts asserted with `assertNumQueries` |

## Run it

```bash
python manage.py test episodes.ep06_q_objects
```
