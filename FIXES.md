# FIXES.md

## FIX 1 — Committed .env file with real credentials
**File:** `api/.env` | **Line:** 1-2
**Problem:** Real password committed to the repository — critical security violation.
**Fix:** Deleted `api/.env`. Added `.env` to `.gitignore`. Created `.env.example` with placeholders.

## FIX 2 — Redis host hardcoded as localhost in API
**File:** `api/main.py` | **Line:** 6
**Problem:** `host="localhost"` fails inside Docker — services must use container service names.
**Fix:** Changed to `REDIS_HOST = os.environ.get("REDIS_HOST", "redis")`.

## FIX 3 — Redis password ignored in API
**File:** `api/main.py` | **Line:** 6
**Problem:** No password argument passed to Redis client — auth always fails when password is set.
**Fix:** Added `password=os.environ.get("REDIS_PASSWORD", None)` to Redis constructor.

## FIX 4 — Missing /health endpoint in API
**File:** `api/main.py`
**Problem:** No health endpoint — Docker HEALTHCHECK and depends_on service_healthy both fail.
**Fix:** Added `GET /health` endpoint that pings Redis and returns 200 or 503.

## FIX 5 — Redis host hardcoded as localhost in worker
**File:** `worker/worker.py` | **Line:** 5
**Problem:** Same as FIX 2 — breaks inside Docker containers.
**Fix:** Changed to read REDIS_HOST, REDIS_PORT, REDIS_PASSWORD from environment variables.

## FIX 6 — Redis password ignored in worker
**File:** `worker/worker.py` | **Line:** 5
**Problem:** Password env var never passed to Redis client.
**Fix:** Added `password=REDIS_PASSWORD` to Redis constructor.

## FIX 7 — signal module imported but never used
**File:** `worker/worker.py` | **Line:** 4
**Problem:** No signal handlers registered — worker cannot shut down gracefully on SIGTERM.
**Fix:** Implemented SIGTERM and SIGINT handlers that set running=False for clean exit.

## FIX 8 — Missing __main__ guard in worker
**File:** `worker/worker.py`
**Problem:** Infinite loop runs at import time — breaks test runners and linters.
**Fix:** Wrapped main loop in `if __name__ == "__main__":`.

## FIX 9 — API_URL hardcoded as localhost in frontend
**File:** `frontend/app.js` | **Line:** 5
**Problem:** `http://localhost:8000` fails inside Docker — must use service name.
**Fix:** Changed to `process.env.API_URL || "http://api:8000"`.

## FIX 10 — Missing /health endpoint in frontend
**File:** `frontend/app.js`
**Problem:** No health endpoint for Docker HEALTHCHECK.
**Fix:** Added `GET /health` route returning `{"status": "ok"}`.

## FIX 11 — Unpinned dependency versions
**File:** `api/requirements.txt`, `worker/requirements.txt`
**Problem:** No version pins — builds are not reproducible.
**Fix:** Pinned all dependencies to specific versions.

## FIX 12 — .decode() called on already-decoded string
**File:** `api/main.py` | **Line:** 18
**Problem:** With decode_responses=True, Redis already returns strings — .decode() raises AttributeError.
**Fix:** Added decode_responses=True to Redis constructor and removed manual .decode() call.
