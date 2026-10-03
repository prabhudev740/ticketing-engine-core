# ticketing-engine-core

### File Structure
```
ticketing-engine-core/
├── .env.example                               # Global environment configuration template
├── .gitignore
├── Makefile                                   # Dev commands (make up, make test, make migrate)
├── docker-compose.yml                         # Local infrastructure orchestration
│
├── deploy/                                    # (Week 12) K8s manifests & helm charts
│   ├── base/
│   │   ├── configmaps.yaml
│   │   ├── secrets.yaml
│   │   └── services.yaml
│   └── overlays/
│       ├── local/
│       └── staging/
│
├── infrastructure/                            # Infrastructure configurations
│   ├── consul/
│   │   └── consul-config.json                 # (Week 1) Local Consul agent setup
│   ├── debezium/
│   │   └── postgres-connector.json            # (Week 6) Redpanda Connect / CDC setup
│   ├── elasticsearch/
│   │   └── mappings.json                      # (Week 7) Search index mappings
│   ├── prometheus/
│   │   └── prometheus.yml                     # (Week 11) Metrics scraping configs
│   ├── grafana/
│   │   └── dashboards/                        # (Week 12) Provisioned JSON dashboards
│   │       ├── api_overview.json
│   │       └── pipelines_and_queues.json
│   └── redpanda/
│       └── redpanda-connect.yaml              # (Week 6) CDC stream routing
│
├── services/                                  # Distributed backend microservices
│   ├── gateway/                               # (Week 1) Main Entrypoint & Auth Service
│   │   ├── Dockerfile
│   │   ├── pyproject.toml
│   │   ├── alembic.ini
│   │   ├── alembic/
│   │   │   ├── env.py
│   │   │   └── versions/
│   │   │       └── 001_create_users_table.py
│   │   └── app/
│   │       ├── __init__.py
│   │       ├── main.py                        # FastAPI lifespan, router mounting & Consul
│   │       ├── config.py                      # Pydantic Settings (.env validator)
│   │       ├── core/
│   │       │   ├── database.py                # Async PostgreSQL connection engine
│   │       │   ├── cache.py                   # Async Redis connection client
│   │       │   ├── security.py                # JWT & bcrypt hashing logic
│   │       │   └── consul.py                  # Service registry & health check publisher
│   │       ├── models/
│   │       │   ├── __init__.py
│   │       │   └── user.py                    # SQLAlchemy User ORM model
│   │       ├── schemas/
│   │       │   ├── __init__.py
│   │       │   ├── auth.py                    # Login/Register request/response schemas
│   │       │   └── user.py                    # User profile schemas
│   │       ├── api/
│   │       │   ├── dependencies.py            # get_db, get_redis, get_current_user
│   │       │   └── v1/
│   │       │       ├── __init__.py
│   │       │       ├── router.py              # Root v1 APIRouter
│   │       │       ├── health.py              # Health check endpoint
│   │       │       └── auth.py                # Register, login, logout, me routes
│   │       └── utils/
│   │           └── exceptions.py              # Custom HTTP error exceptions
│   │
│   ├── catalog-service/                       # (Week 2) Unstructured event catalog (MongoDB)
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── app/
│   │       ├── main.py
│   │       ├── models/                        # Beanie/Motor Mongo models
│   │       └── api/v1/
│   │
│   ├── booking-service/                       # (Weeks 3 & 4) Locking, Outbox & RabbitMQ
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── app/
│   │       ├── main.py
│   │       ├── core/
│   │       │   └── lock.py                    # Redlock algorithm implementation
│   │       ├── models/                        # Orders & Outbox tables
│   │       └── workers/
│   │           ├── outbox_publisher.py        # Outbox polling worker
│   │           └── ticket_generator.py        # RabbitMQ PDF worker
│   │
│   ├── search-service/                        # (Weeks 7 & 8) Meilisearch & Qdrant Engine
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── app/
│   │       ├── main.py
│   │       ├── search/
│   │       │   └── meili_client.py            # Typo-tolerant text search
│   │       └── vector/
│   │           ├── embedder.py                # sentence-transformers embedding
│   │           └── qdrant_client.py           # Cosine similarity vector search
│   │
│   └── stream-consumers/                      # (Week 5) Redpanda stream consumers
│       ├── Dockerfile
│       ├── requirements.txt
│       └── app/
│           ├── capacity_calculator.py         # Partitioned group consumer
│           └── loyalty_worker.py
│
└── tests/                                     # Root integration and regression suite
    ├── conftest.py                            # Async HTTP client, DB/Redis fixtures
    ├── integration/
    │   ├── test_health.py                     # (Week 1)
    │   ├── test_auth.py                       # (Week 1)
    │   ├── test_locking.py                    # (Week 3)
    │   ├── test_outbox.py                     # (Week 4)
    │   └── test_search_cqrs.py                # (Week 7)
    └── load/
        └── locustfile.py                      # (Week 9 & 12) Stress testing scripts
```