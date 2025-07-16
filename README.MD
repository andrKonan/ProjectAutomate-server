# Project Automate

A FastAPI-powered “resource bot” game server with SQLAlchemy 2.0 typed ORM, and Pydantic v2 schemas. Also uses GraphQL for comunication 
Players register, build bots, explore a fog-of-war map, gather/transform resources, and level up bots & buildings.

---

## Table of Contents

1. [Tech Stack](#tech-stack)  
2. [Project Structure](#project-structure)  
3. [Getting Started](#getting-started)  
   1. [Prerequisites](#prerequisites)  
   2. [Installation](#installation)  
   3. [Run the Server](#run-the-server)  
4. [Authentication](#authentication)
5. [Switching to PostgreSQL](#switching-to-postgresql)  
6. [License](#license)

---

## Tech Stack
- **Python** 3.10+
- **FastAPI** ≥ 0.110
- **Uvicorn**
- **SQLAlchemy** 2.0 typed ORM (`Mapped`, `mapped_column`)
- **Pydantic** v2 for request/response schemas
- **Graphene** for GraphQL
- **SQLite** (default) via `aiosqlite`
- **PostgreSQL** support via `asyncpg`


---

## Project Structure
```
server/
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── bots.py
│   ├── buildings.py
│   ├── client.py
│   ├── items.py
│   ├── recipes.py
│   └── structures.py
│
├── __init__.py
├── config.py
├── database.py
├── errors.py
├── main.py
├── readme.md
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.10+ installed  
- (Optional) Virtual environment tool (`venv`, `poetry`, etc.)

### Installation

1. **Clone the repo**  
```bash
git clone https://github.com/andrKonan/ProjectAutomate-server.git ProjectAutomate/server
cd ProjectAutomate/server
```

2. **Create & activate virtualenv**
```bash
python -m venv .venv
source .venv/bin/activate       # Linux & macOS
.venv\Scripts\activate          # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Run the Server
Run the server from the ProjectAutomate folder
```bash
uvicorn server.main:app --reload
```

 - App URL: http://127.0.0.1:8000/
 - Interactive docs:
   - Swagger UI at http://127.0.0.1:8000/docs
   - ReDoc at http://127.0.0.1:8000/redoc

---

## Authentication

All endpoints (except POST /register) require an X-Auth-Token header:
```yaml
X-Auth-Token: <your_token_here>
```