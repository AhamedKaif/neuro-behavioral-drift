# Neuro-Behavioral Drift API - Load Testing Report

This report presents the performance baseline and analysis of the **Neuro-Behavioral Drift API** under concurrent user load, executed using Grafana k6.

---

## 📊 Test Configuration
- **Virtual Users (VUs):** 100 concurrent users
- **Duration:** 1 minute (continuous)
- **Target URL:** `http://localhost:5000` (Flask Backend)
- **Scenarios Tested:**
  1. Authenticating & generating a JWT token (Setup phase)
  2. Fetching user dashboard data (`GET /api/dashboard`)
  3. Fetching user profile details (`GET /api/profile`)
  4. Submitting user behavioral metrics and triggering real-time ML model inference (`POST /api/metrics`)

---

## 📈 Performance Summary

| Metric | Result | Interpretation |
| :--- | :--- | :--- |
| **Total Requests Sent** | **3,370** | High-throughput load successfully delivered. |
| **Requests Per Second (RPS)** | **52.77 req/sec** | The API successfully processed over 50 requests per second. |
| **Average Response Time** | **1,720 ms (1.72s)** | Average round-trip time across all endpoints. |
| **Median Response Time** | **600.38 ms** | 50% of requests resolved in under 600ms. |
| **95th Percentile (p95)** | **6,330 ms (6.33s)** | Under heavy load, response times spiked due to resource queuing. |
| **Minimum Response Time** | **12.77 ms** | Response time for fast cached/read-only responses under low lock contention. |
| **Maximum Response Time** | **8,090 ms (8.09s)** | Peak response time, largely caused by write transaction timeouts. |
| **Overall Request Success Rate** | **83.86%** | 2,825 out of 3,370 requests successfully completed (200/201). |
| **Overall Request Failure Rate** | **16.14%** | 544 out of 3,370 requests failed (returned 500/locking errors). |

---

## 🔍 Endpoint Analysis

### 1. Dashboard (`GET /api/dashboard`)
- **Success Rate:** **100%** (3,556 / 3,556 checks passed)
- **Analysis:** Read-only queries executed extremely fast and did not suffer from write contention. 

### 2. User Profile (`GET /api/profile`)
- **Success Rate:** **100%** (3,556 / 3,556 checks passed)
- **Analysis:** Read-only user data fetching is highly performant and stable under concurrency.

### 3. Ingest Metrics (`POST /api/metrics`)
- **Success Rate:** **51.56%** (579 passed / 544 failed)
- **Analysis:** This endpoint experienced a **48.44% failure rate**.
- **Root Cause:** 
  1. **SQLite Database Locking:** The ingestion endpoint performs `INSERT` transactions into both the `behavioral_metrics` and `predictions` tables. Because SQLite uses file-level locking, it only allows a single write transaction at a time. Under 100 concurrent VUs, database write contention caused `database is locked` errors (yielding HTTP 500 errors).
  2. **Inference Overhead:** Running ML predictions on the CPU for every incoming request adds compute overhead that, when coupled with DB locks, increases response times to a maximum of 8.09 seconds.

---

## 💡 Recommendations for Optimization

1. **Implement Write Queue / Message Broker:**
   Instead of writing metrics to SQLite synchronously during the HTTP request, push metrics to an in-memory queue (like Redis or a background thread-safe Python Queue) and process them asynchronously via a worker process.

2. **Transition to PostgreSQL in Production:**
   SQLite is ideal for development but has severe write concurrency limits. Upgrading to PostgreSQL will enable row-level locking and concurrent write transactions.

3. **In-Memory Model Caching and Batching:**
   Batch inference requests or execute them in a separate service to avoid blocking the main web server threads.
