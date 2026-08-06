# System Design Interview Guide: Back-of-the-Envelope Calculations

## Why estimate?

Back-of-the-envelope calculations help you estimate scale quickly so you
can justify architectural decisions rather than guessing.

## Golden constants

-   30 days ≈ 2,592,000 seconds ≈ **2.5 million seconds**
-   **1 RPS ≈ 2.5 million requests/month**
-   **400 RPS ≈ 1 billion requests/month**

## Conversion formulas

### Monthly to RPS

`RPS = Monthly Requests / 2,592,000`

Shortcut: `RPS ≈ Billions per month × 400`

### RPS to Monthly

`Monthly ≈ RPS × 2.5 million`

## Example (Twitter)

Input assumptions: - 100M active users - 500M tweets/day - 15B
tweets/month - Avg fanout = 10 - 250B timeline reads/month - 10B
searches/month

### Throughput

  Metric             Calculation                  Result
  ---------------- ------------- -----------------------
  Tweet writes          15 × 400        6,000 tweets/sec
  Fanout writes        150 × 400   60,000 deliveries/sec
  Timeline reads       250 × 400       100,000 reads/sec
  Search                10 × 400      4,000 searches/sec

## Storage estimation

Assume one tweet: - Tweet ID: 8 B - User ID: 32 B - Text: 140 B - Media:
\~10 KB

Average tweet size ≈ **10 KB**

Daily: `500M × 10KB = ~5 TB/day`

Monthly: `~150 TB/month`

3 years: `150 × 36 = 5.4 PB`

------------------------------------------------------------------------

# How to approach any system design interview

1.  Clarify requirements.
2.  Estimate traffic (reads, writes, storage).
3.  Identify bottleneck (read-heavy, write-heavy, storage-heavy).
4.  Design high-level architecture.
5.  Choose databases.
6.  Add cache.
7.  Scale services.
8.  Discuss sharding/replication.
9.  Mention monitoring and trade-offs.

------------------------------------------------------------------------

# Choosing databases

Use SQL when: - Transactions - Strong consistency - Joins

Use NoSQL when: - Massive scale - Horizontal sharding - Simple access
patterns

Twitter timelines/tweets are commonly modeled in distributed NoSQL
because of scale.

------------------------------------------------------------------------

# How many application servers?

Don't memorize numbers.

Estimate:

    Servers = Peak RPS / Capacity per server

Example:

Peak = 100,000 RPS

One server handles = 2,000 RPS

Servers = 50

Add 20--50% headroom.

------------------------------------------------------------------------

# How to size the database

Estimate storage growth first.

Example:

150 TB/month

1.8 PB/year

If one node stores 10 TB:

180 data nodes (before replication)

With 3x replication:

540 physical nodes

In interviews, explain **sharding strategy**, not exact node counts.

------------------------------------------------------------------------

# Sharding

Common shard keys: - User ID - Tweet ID

Good shard key: - Even distribution - Avoid hotspots - Supports common
queries

Avoid timestamp-only shard keys because hot traffic lands on one shard.

------------------------------------------------------------------------

# Replication

Typical: - 3 replicas - Leader/follower or quorum

Benefits: - High availability - Read scaling - Disaster recovery

------------------------------------------------------------------------

# Cache strategy

Cache hot data, not all data.

Examples: - User profile - Home timeline - Popular tweets

Flow:

Client → API → Redis → Database

Target high cache hit rate to reduce database load.

------------------------------------------------------------------------

# Fanout

User posts

↓

Queue (Kafka)

↓

Fanout workers

↓

Followers' timelines

Asynchronous fanout keeps tweet posting fast.

------------------------------------------------------------------------

# Search

Separate search system from OLTP database.

Typical: - Elasticsearch - OpenSearch

Index asynchronously.

------------------------------------------------------------------------

# Storage

Store media in object storage.

Database stores only metadata and object URL.

------------------------------------------------------------------------

# Checklist

-   Requirements
-   APIs
-   Traffic estimates
-   Storage estimates
-   Read/write ratio
-   Database choice
-   Cache
-   Load balancer
-   Message queue
-   Sharding
-   Replication
-   Scaling
-   Monitoring
-   Trade-offs

The goal of back-of-the-envelope calculations is not perfect accuracy
but to justify architecture with reasonable estimates.
