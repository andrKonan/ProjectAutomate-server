# ProjectAutomate Server

A FastAPI-powered, Strawberry-GraphQL backend for the Resource Bot game. Players can register, build bots, explore a fog-of-war map, gather & transform resources, and upgrade buildings. All via a modern async GraphQL API.

---

## Table of Contents

- [Tech Stack](#tech-stack)  
- [Project Structure](#project-structure)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Installation](#installation)  
  - [Configuration](#configuration)  
  - [Running the Server](#running-the-server)  
  - [Automatic seeding](#automatic-seeding)  
- [GraphQL API](#graphql-api)  
  - [Endpoint](#endpoint)  
  - [Authentication](#authentication)  
  - [Permissions](#permissions)  
- [Database](#database)  
- [Switching to PostgreSQL](#switching-to-postgresql)  
- [Testing](#testing)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Tech Stack

- **Python** 3.10+  
- **FastAPI** for HTTP server  
- **Strawberry** for GraphQL schema & execution  
- **SQLAlchemy 2.0** (async) for ORM  
- **SQLite** (default, `game.db`)  
- **PostgreSQL** via `asyncpg` (optional)  
- **Uvicorn** as ASGI server  

---

## Project Structure
```
server/
├── database/
│   ├── models/               # SQLAlchemy models (bots, buildings, etc.)
│   ├── services/             # CRUD logic, database interaction
│   └── domains/              # Buisness/game logic
├── graphql/
│   ├── resolvers/            # GraphQL query/mutation logic
│   ├── schemas/              # GraphQL schemas for queries
│   ├── inputs/               # GraphQL inputs for mutations
│   ├── permissions.py        # Permission classes
│   └── graphql.py            # Schema & router setup
├── seed/                     # YAML data for initial DB seeding
│   ├── bots.yaml
│   ├── items.yaml
│   └── structures.yaml
├── workers/
│   └── seed.py               # Worker that will run on every server start
├── config.py                 # Environment settings
├── main.py                   # App entry point
└── requirements.txt          # Frozen packages
```

---

## Getting Started

### Prerequisites

- Python 3.10 or newer  
- (Optional) Virtual environment tool: `venv`, `poetry`, etc.

### Installation

1. Clone repository
```bash
git clone https://github.com/your-username/ProjectAutomate-server.git server
cd server
```

2. Create & activate virtual environment
```bash
python -m venv .venv  
# Linux/macOS  
source .venv/bin/activate  
# Windows  
.venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

### Configuration

Edit **`config.py`** or set environment variables as needed:

- `DATABASE_URL` – e.g. `sqlite+aiosqlite:///./game.db` (default)  
- (Optional) for PostgreSQL:  
  `postgresql+asyncpg://user:pass@host:port/dbname`

### Running the Server

Start the ASGI server with hot reload:  
```bash
uvicorn main:app --reload
```

- **GraphiQL UI:**  http://127.0.0.1:8000/graphql  
- **OpenAPI docs:**  http://127.0.0.1:8000/docs  

### Automatic seeding

The server has a worker that will run on each start up.
The worker reads YAML files from the seed/ directory 
and uses service-layer logic to insert or update data.

It's:
 - Idempotent: You can run it multiple times safely.
 - Validates referenced types by name (e.g., items in recipes).
 - Logs skipped entries and handles missing types gracefully.

---

## GraphQL API

### Endpoint

All GraphQL operations are served at:

    POST /graphql  
    GET  /graphql    ← GraphiQL playground (if enabled)

### Authentication

- **Register** via the public `createClient` mutation to receive your token.
- **Include** the token on every subsequent request in the `Authorization` header:  
      Authorization: Bearer <your_token_here>

Your token is looked up in `get_context` (in `context.py`), and `current_client` is injected into each resolver’s context.

### Permissions

I leverage Strawberry’s `BasePermission` classes:

- **IsAuthenticated**: blocks any operation when `current_client` is `null`.  
- **IsClientOwner**: ensures the `id` argument matches `current_client.id`, preventing one user from mutating another’s data.

Applied like:
```py
@strawberry.mutation(permission_classes=[IsAuthenticated, IsClientOwner])
async def update_client(...): ...
```

---

## Database

- Local development uses **SQLite** (`game.db`) – no setup required.  
- Each request gets an **AsyncSession** via `database.py`, injected into `context`.

---

## Switching to PostgreSQL

1. Install `asyncpg`:
```bash
pip install asyncpg
```

2. Update `DATABASE_URL` in `config.py` or your environment:
```
postgresql+asyncpg://user:password@host:5432/your_db
```

3. Restart the server.

---

## Testing

_Coming soon_

Testing will cover both unit and integration layers, including:

- GraphQL resolver behavior
- Database service logic
- Permission enforcement
- Seeder validation

> 🔧 Stay tuned – test setup and example cases will be added.

---

## Contributing

1. Fork the repo  
2. Create a feature branch  
3. Install & run tests just when they will be ready :) 
4. Submit a pull request

Please follow existing code style and add tests for new features.

---

## License

This project is licensed under the MIT License.  
See the LICENSE file for details.
