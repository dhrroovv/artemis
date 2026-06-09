# Artemis - Search & Discovery Platform

A backend-first search platform built on top of a product catalog, supporting lexical search, semantic search, autosuggestions, analytics, authentication, background processing, and search quality monitoring.

The goal of this project is not simply to expose a `/search` endpoint, but to build the supporting infrastructure required by a modern search system, including data ingestion, indexing, ranking, caching, analytics, and observability.

---

## Motivation

Most search implementations stop at querying a database and returning results.

Real-world search systems require much more:

- Continuous synchronization from source systems
- Search indexing pipelines
- Query analytics
- Ranking strategies
- Autosuggestions
- Semantic retrieval
- Background processing
- Rate limiting
- Authentication and authorization
- Monitoring and observability

This project aims to explore those challenges while remaining approachable as a standalone backend application.

---

## High-Level Architecture

```text
                    ┌─────────────────┐
                    │ Authentication  │
                    └────────┬────────┘
                             │
                             ▼

                    ┌─────────────────┐
                    │   Search API    │
                    └────────┬────────┘
                             │

        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼

  Lexical Search      Semantic Search      Autosuggest
        │                    │                    │
        └────────────┬───────┴────────────┬───────┘
                     ▼                    ▼

                Ranking Layer       Cache Layer
                     │
                     ▼

                 Search Results
```

### Data Pipeline

```text
Catalog Source
      │
      ▼

Catalog Sync Worker
      │
      ▼

Application Database
      │
      ├── Search Index Updates
      ├── Embedding Generation
      └── Analytics Processing
```

---

## Core Components

### Authentication & Session Management

Responsible for:

- User registration
- User login
- JWT access tokens
- Refresh tokens
- Session management
- Logout and session revocation
- Role-based access control

Planned endpoints:

```http
POST /auth/register
POST /auth/login
POST /auth/refresh
POST /auth/logout
GET  /auth/me
GET  /auth/sessions
DELETE /auth/sessions/{id}
```

---

### Catalog Ingestion

Responsible for synchronizing catalog data from the source system into the application's data store.

Features:

- Periodic synchronization
- Incremental updates
- Retry handling
- Background processing

Future considerations:

- Change Data Capture (CDC)
- Event-driven synchronization

---

### Search Engine

Provides search capabilities across the catalog.

Features:

- Keyword search
- Product discovery
- Relevance ranking
- Filtering
- Pagination

Planned search strategies:

#### Lexical Search

Traditional text-based retrieval:

- PostgreSQL Full Text Search
- BM25
- Fuzzy matching
- Synonym support

#### Semantic Search

Embedding-based retrieval:

- Product embeddings
- Query embeddings
- Vector similarity search

#### Hybrid Search

Combines lexical and semantic search for improved relevance.

Potential ranking techniques:

- BM25
- Vector similarity
- Popularity signals
- Freshness signals
- Reciprocal Rank Fusion (RRF)

---

### Autosuggest

Provides real-time query suggestions.

Example:

```text
Input: "sun"

Suggestions:
- sunscreen
- sunblock
- sun protection
```

Potential ranking signals:

- Search frequency
- Click-through rate
- Recent trends

---

### Analytics

Captures user search behavior to improve search quality.

Tracked events:

```text
Query
Timestamp
User
Results Returned
Clicked Product
Search Latency
```

Potential dashboards:

- Most searched queries
- Zero-result searches
- Popular products
- Click-through rates
- Search performance metrics

---

### Background Workers

Asynchronous workers process tasks that should not run during request handling.

Examples:

#### Catalog Sync Worker

```text
Source Catalog
      ↓
Sync
      ↓
Application Database
```

#### Embedding Worker

```text
Product Updated
      ↓
Generate Embedding
      ↓
Store Vector
```

#### Analytics Worker

```text
Search Event
      ↓
Queue
      ↓
Aggregation
```

---

## Planned Technology Stack

### API Layer

- FastAPI

### Database

- PostgreSQL

### Cache

- Redis

### Background Processing

- ARQ
- Redis Queue

### Vector Search

Potential options:

- pgvector
- Qdrant

### Observability

- OpenTelemetry
- Prometheus
- Grafana

### Infrastructure

- Docker
- Docker Compose

---

## Security

Planned security features:

- JWT authentication
- Refresh token rotation
- Session revocation
- Password hashing
- Role-based access control
- API rate limiting
- Request validation

---

## API Roadmap

### Search

```http
GET /search
GET /search/suggestions
```

### Analytics

```http
GET /analytics/top-searches
GET /analytics/zero-results
GET /analytics/popular-products
```

### Admin

```http
POST /admin/reindex
POST /admin/sync-catalog
GET  /admin/jobs
```

---

## Development Roadmap

### Phase 1

- Authentication
- Catalog ingestion
- Basic search
- Autosuggest
- PostgreSQL integration

### Phase 2

- Full-text search
- Ranking improvements
- Fuzzy matching
- Synonym support

### Phase 3

- Background workers
- Redis integration
- Search analytics

### Phase 4

- Embeddings
- Vector search
- Hybrid retrieval

### Phase 5

- Caching
- Observability
- Metrics
- Tracing
- Performance optimization

---

## Learning Objectives

This project is intended to provide hands-on experience with:

- Backend architecture
- Authentication systems
- Session management
- Search systems
- Information retrieval
- Vector databases
- Background processing
- Distributed system concepts
- Caching strategies
- Observability
- Production-grade API design
- Data pipelines
- Search analytics
- Ranking systems

---

## Current Status

Project is currently in the planning and architecture phase.
