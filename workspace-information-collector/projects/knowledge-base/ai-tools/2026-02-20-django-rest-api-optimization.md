# How to Optimize Django REST APIs for Performance

- **Date:** 2026-02-20
- **Source:** https://www.freecodecamp.org/news/how-to-optimize-django-rest-apis-for-performance/
- **Tags:** #django #api-performance #backend #optimization #caching

---

## Key Takeaways (Detailed)

### 1. Root Causes of Slow Django APIs

| Cause | Description | Impact |
|-------|-------------|--------|
| **N+1 Query Problem** | Accessing related objects in loops triggers separate query per item | 100 posts = 101 queries |
| **Returning Too Much Data** | Fetching thousands of records at once without pagination | Memory bloat, slow serialization |
| **Repeated Expensive Computations** | Recalculating same values on every request | Wasted CPU cycles |

> **Django is fast by default, but it does exactly what you ask.** If your endpoint triggers 300 queries, Django will happily run all 300.

---

### 2. Profiling Tools You MUST Use

#### A. Django Debug Toolbar
- Shows SQL query count, execution time, duplicate queries
- **Install:** `pip install django-debug-toolbar`
- **Warning sign:** 150+ queries for a single request = N+1 problem

#### B. Query Count Measurement
```python
from django.db import connection

# Add to any view
print(f"Total queries: {len(connection.queries)}")
```

#### C. Response Time Profiling
```python
import time
start = time.time()
# ... your code ...
print(f"Response time: {time.time() - start:.4f}s")
```

**Key insight:** If queries are fast (50ms) but total response is slow (1.2s), bottleneck is serialization or Python logic — NOT the database.

---

### 3. Query Optimization Techniques

#### select_related (ForeignKey / OneToOne)
```python
# ❌ BAD: 101 queries for 100 posts
posts = Post.objects.all()
for p in posts:
    print(p.author.name)

# ✅ GOOD: 1 query with JOIN
posts = Post.objects.select_related("author")
```
- Performs SQL JOIN
- Use for: ForeignKey, OneToOne relationships

#### prefetch_related (ManyToMany / Reverse FK)
```python
# ❌ BAD: 1 + N queries
posts = Post.objects.all()
for p in posts:
    print(p.tags.all())

# ✅ GOOD: 2 queries total
posts = Post.objects.prefetch_related("tags")
```
- Separate queries, combined in Python
- Use for: ManyToMany, reverse ForeignKey

#### Common Mistakes to Avoid
- ❌ Forgetting serializers can trigger extra queries
- ❌ Using select_related on ManyToMany (doesn't work)
- ❌ Assuming Django auto-optimizes
- ❌ Not checking query count after adding serializers

---

### 4. Caching Strategies

#### Cache Layers (Fast → Slow)
1. **Client-side** — HTTP headers (Cache-Control)
2. **CDN** — static assets closer to users
3. **Backend** — Redis/memcached for API responses

#### Django Cache Types
```python
# Per-view caching
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 15 minutes
def my_view(request):
    ...

# Low-level caching (most flexible)
from django.core.cache import cache
cache.set('my_key', data, 3600)
```

#### When to Use Redis
- ✅ Data read frequently, changes infrequently
- ✅ Low latency is critical
- ✅ Need shared cache across multiple servers
- ✅ Want expiration/eviction policies

#### Common Caching Mistakes
- ❌ Caching everything blindly
- ❌ Forgetting cache invalidation (stale data!)
- ❌ Caching when query optimization would suffice

---

### 5. Pagination

**Always paginate list endpoints unless there's a strong reason not to.**

Benefits:
- Reduces database load
- Reduces memory usage
- Reduces serialization time
- Reduces network transfer size

---

### 6. Load Testing

**Always measure before/after optimization.**

Questions to answer:
- How many requests/second can API handle?
- Where does it break under load?
- Did optimizations actually improve performance?

Tools: Apache Bench, locust, k6

---

## Actions to Take (Priority Order)

### 🔴 High Priority — Do First

| Action | Why | How |
|--------|-----|-----|
| **Add query counting to views** | Confirm if you have N+1 problem | `len(connection.queries)` |
| **Install Django Debug Toolbar** | Visual profiling during dev | `pip install django-debug-toolbar` |
| **Add select_related to FK queries** | Biggest query reduction | `.select_related("author")` |
| **Add prefetch_related to M2M** | Fix M2M N+1 | `.prefetch_related("tags")` |

### 🟡 Medium Priority — Next

| Action | Why | How |
|--------|-----|-----|
| **Paginate list endpoints** | Prevent memory bloat | DRF pagination classes |
| **Add per-view caching** | Reduce repeated computation | `@cache_page(60 * 15)` |
| **Set up Redis for production** | Shared cache, low latency | `django-redis` package |
| **Implement cache invalidation** | Prevent stale data | Time-based or event-based |

### 🟢 Low Priority — Later

| Action | Why | How |
|--------|-----|-----|
| **Load test your API** | Validate improvements | k6, locust |
| **Optimize serializers** | Reduce serialization time | Use `select_fields` in serializers |
| **Add database indexes** | Speed up slow queries | `db_index=True` on frequently queried fields |

---

## Quick Wins Checklist

- [ ] Count queries on slow endpoints
- [ ] Replace `.all()` with `.select_related()` for ForeignKey
- [ ] Replace `.all()` with `.prefetch_related()` for ManyToMany
- [ ] Add pagination to list endpoints
- [ ] Add `@cache_page()` to rarely-changing views
- [ ] Set up Redis in production
- [ ] Run load tests before/after changes

---

## Related Topics to Explore

- Django ORM optimization: https://docs.djangoproject.com/en/stable/topics/db/optimization/
- DRF Performance: https://www.django-rest-framework.org/topics/performance/
- Redis caching with Django: django-redis package
- Load testing tools: k6, locust, Apache Bench
