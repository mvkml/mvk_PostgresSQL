# PostgreSQL Documentation

## What is PostgreSQL?

PostgreSQL is a powerful, open-source **relational database management system (RDBMS)** that uses Structured Query Language (SQL) for managing and querying data. It's known for its reliability, robustness, and advanced features.

### Key Characteristics

- **Open Source**: Free to use, modify, and distribute
- **ACID Compliant**: Ensures data integrity through Atomicity, Consistency, Isolation, and Durability
- **Highly Extensible**: Supports custom data types, operators, and functions
- **SQL Compliant**: Adheres to SQL standards while offering advanced features
- **Cross-Platform**: Runs on Linux, Windows, macOS, and other operating systems
- **Scalability**: Handles large databases and concurrent users efficiently
- **Advanced Features**: Supports JSON, full-text search, arrays, and more

### Why Use PostgreSQL?

1. **Reliability**: Proven track record in production environments
2. **Performance**: Efficient query optimization and indexing
3. **Security**: Row-level security, role-based access control
4. **Flexibility**: JSON/JSONB support for semi-structured data
5. **Community**: Active and supportive community with regular updates
6. **Cost-Effective**: No licensing fees

## Installation & Setup

### Windows Installation

1. Download PostgreSQL installer from [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
2. Run the installer and follow the setup wizard
3. During installation, set a password for the default `postgres` user
4. Choose installation directory (default: `C:\Program Files\PostgreSQL`)
5. Select components (Server, pgAdmin 4, CLI Tools, etc.)
6. Complete the installation and verify by opening pgAdmin 4

### Basic Configuration

```bash
# Connect to PostgreSQL via command line
psql -U postgres -h localhost

# Create a new database
CREATE DATABASE myapp;

# Create a new user
CREATE USER myuser WITH PASSWORD 'password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE myapp TO myuser;
```

## Common PostgreSQL Commands

### Database Management

```sql
-- List all databases
\l

-- Create database
CREATE DATABASE database_name;

-- Delete database
DROP DATABASE database_name;

-- Connect to database
\c database_name
```

### Table Operations

```sql
-- Create table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- View table structure
\d table_name

-- Insert data
INSERT INTO users (username, email) VALUES ('john_doe', 'john@example.com');

-- Query data
SELECT * FROM users;

-- Update data
UPDATE users SET email = 'newemail@example.com' WHERE id = 1;

-- Delete data
DELETE FROM users WHERE id = 1;
```

### User Management

```sql
-- Create user
CREATE USER newuser WITH PASSWORD 'secure_password';

-- Grant privileges
GRANT CONNECT ON DATABASE mydb TO newuser;
GRANT USAGE ON SCHEMA public TO newuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO newuser;

-- List users
\du

-- Drop user
DROP USER username;
```

## PostgreSQL with Python (FastAPI Project)

### Required Package

```bash
pip install psycopg2-binary
# or for async support
pip install asyncpg
```

### Connection Example

```python
import psycopg2
from psycopg2 import sql

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="myapp",
        user="myuser",
        password="password",
        port=5432
    )

# Using connection
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM users;")
rows = cursor.fetchall()
cursor.close()
conn.close()
```

### Async Connection with asyncpg (Recommended)

```python
import asyncpg

async def init_db():
    pool = await asyncpg.create_pool(
        user='myuser',
        password='password',
        database='myapp',
        host='localhost',
        port=5432
    )
    return pool

async def fetch_users(pool):
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM users;')
    return rows
```

## Integration with VishAgent Project

### Database Configuration in `config.py`

```python
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "vishagent_db"
DB_USER = "vishagent_user"
DB_PASSWORD = "secure_password"
DB_POOL_SIZE = 10
DB_MAX_OVERFLOW = 20
```

### Setup Steps

1. Install PostgreSQL locally or use Docker
2. Create database: `CREATE DATABASE vishagent_db;`
3. Create user: `CREATE USER vishagent_user WITH PASSWORD 'password';`
4. Grant privileges
5. Update configuration in `app/core/config.py`
6. Run migrations (if using Alembic)

## Useful Resources

- **Official Documentation**: https://www.postgresql.org/docs/
- **pgAdmin 4**: Web-based administration tool for PostgreSQL
- **DBeaver**: Free database management tool with PostgreSQL support
- **SQLAlchemy ORM**: Python ORM for database operations

## PostgreSQL Tools & GUI

- **pgAdmin 4**: Web interface (included with installer)
- **DBeaver**: Universal database tool
- **DataGrip**: JetBrains IDE for databases
- **VS Code Extension**: SQLTools PostgreSQL extension

---

## Developer Profile

### Vishnu Kiran M

**Role**: AI Solutions Developer  
**Project**: VishAgent - FastAPI-based AI Agent System for Claim Policy Analysis  
**Specialization**: AI/ML Integration, LLM Tool Calling, LangGraph Implementation

**Tech Stack**:
- Backend: FastAPI, Python 3.x
- Database: PostgreSQL
- AI/ML: OpenAI API, LangChain, LangGraph
- Architecture: Layered Architecture (Routes → Services → Repositories)

**Key Contributions**:
- Building AI agent systems for claim policy validation
- Implementing OpenAI function calling patterns
- Developing LangGraph-based workflow automation
- FastAPI API endpoint development and integration

**Project Structure Expertise**:
- API Layer: Routes with Pydantic models
- Service Layer: Business logic and LLM integration
- Repository Layer: Database abstraction and CRUD operations
- Core Config: Environment and application settings management

**Contact & Repository**:
- Project Location: `C:\v\v\learn\lv_python\ai\VishAgent`
- Documentation: `/Documents` folder (including ClaimPolicy, Lan_Graph patterns)

**Current Focus**:
- Transitioning from MCPBot architecture patterns
- Implementing claim validation workflows with LLM integration
- Establishing best practices for LangGraph tool definitions
- PostgreSQL database integration for persistent storage

---

*Last Updated: January 18, 2026*
