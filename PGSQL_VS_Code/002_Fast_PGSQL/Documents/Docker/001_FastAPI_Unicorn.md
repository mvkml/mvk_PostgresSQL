# Uvicorn & FastAPI

## Document Information

**Author:** Vishnu Kiran M  
**Role:** End-to-End AI, Cloud & Big Data Solution Designer  
**Last Updated:** January 17, 2026

---

## What is Uvicorn?

**Uvicorn** is a lightning-fast ASGI (Asynchronous Server Gateway Interface) server implementation, built on top of `uvloop` and `httptools`. It's the recommended server for running FastAPI applications in production.

### Why Uvicorn for FastAPI?

FastAPI is an ASGI framework, which means it's designed to handle asynchronous operations. Traditional WSGI servers (like Gunicorn with sync workers) cannot fully utilize FastAPI's async capabilities. Uvicorn bridges this gap by providing:

- **Native ASGI Support**: Fully compatible with FastAPI's async/await syntax
- **High Performance**: One of the fastest Python web servers available
- **HTTP/1.1 and WebSocket Support**: Real-time communication capabilities
- **Production Ready**: Stable and widely adopted in production environments

---

## How Uvicorn Relates to FastAPI

### The Architecture Stack

```
┌─────────────────────────────────┐
│      FastAPI Application        │  ← Your API Code
├─────────────────────────────────┤
│      ASGI Interface             │  ← Standard Protocol
├─────────────────────────────────┤
│      Uvicorn Server             │  ← ASGI Server
├─────────────────────────────────┤
│      uvloop + httptools         │  ← Performance Layer
├─────────────────────────────────┤
│      Operating System           │  ← Network I/O
└─────────────────────────────────┘
```

### Key Relationship Points

1. **FastAPI creates the ASGI application** - Your code defines routes, dependencies, and business logic
2. **Uvicorn runs the ASGI application** - It handles HTTP requests, manages connections, and invokes your FastAPI code
3. **Async event loop** - Uvicorn manages the event loop that allows FastAPI to handle multiple requests concurrently

---

## Installing Uvicorn

### Basic Installation
```bash
pip install uvicorn
```

### Standard Installation (Recommended)
Includes performance optimizations with `uvloop` and `httptools`:
```bash
pip install "uvicorn[standard]"
```

### With FastAPI
```bash
pip install fastapi "uvicorn[standard]"
```

---

## Running FastAPI with Uvicorn

### Basic Development Mode

```bash
uvicorn main:app --reload
```

**Parameters:**
- `main` - Python module name (main.py)
- `app` - FastAPI instance variable name
- `--reload` - Auto-restart on code changes (development only)

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Key Options:**
- `--host 0.0.0.0` - Listen on all network interfaces
- `--port 8000` - Specify port number
- `--workers 4` - Number of worker processes

### Advanced Configuration

```bash
uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --log-level info \
  --access-log \
  --use-colors \
  --timeout-keep-alive 5
```

---

## Uvicorn Configuration Options

### Common Parameters

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `--host` | Bind socket to this host | 127.0.0.1 | 0.0.0.0 |
| `--port` | Bind socket to this port | 8000 | 8080 |
| `--workers` | Number of worker processes | 1 | 4 |
| `--reload` | Enable auto-reload | False | True |
| `--log-level` | Log level | info | debug |
| `--access-log` | Enable access log | False | True |
| `--proxy-headers` | Enable X-Forwarded-Proto, X-Forwarded-For | False | True |
| `--forwarded-allow-ips` | Trusted proxy IPs | 127.0.0.1 | * |
| `--ssl-keyfile` | SSL key file path | None | /path/to/key.pem |
| `--ssl-certfile` | SSL certificate file path | None | /path/to/cert.pem |

### Programmatic Usage

```python
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True  # Only for development
    )
```

---

## Production Deployment with Uvicorn

### Option 1: Uvicorn with Multiple Workers

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Pros:**
- Simple setup
- Built-in worker management

**Cons:**
- Limited process management features
- No zero-downtime reload

### Option 2: Gunicorn + Uvicorn Workers (Recommended)

```bash
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 60 \
  --graceful-timeout 30
```

**Install:**
```bash
pip install gunicorn uvicorn[standard]
```

**Pros:**
- Better process management
- Graceful restarts
- More configuration options
- Zero-downtime deployments

### Worker Calculation

```python
# Recommended formula
workers = (2 × CPU_cores) + 1

# Example for 4 CPU cores
workers = (2 × 4) + 1 = 9
```

---

## Uvicorn vs Other ASGI Servers

### Uvicorn
- **Best For**: FastAPI applications, high-performance APIs
- **Pros**: Extremely fast, simple configuration, excellent FastAPI integration
- **Cons**: Basic process management

### Hypercorn
- **Best For**: HTTP/2 and HTTP/3 support needed
- **Pros**: Supports newer protocols, Trio/asyncio compatibility
- **Cons**: Slightly slower than Uvicorn

### Daphne
- **Best For**: Django Channels applications
- **Pros**: Django integration, WebSocket support
- **Cons**: Slower performance compared to Uvicorn

---

## FastAPI Application Example with Uvicorn

### main.py

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="My API",
    description="FastAPI with Uvicorn",
    version="1.0.0"
)

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

@app.get("/")
async def root():
    return {"message": "FastAPI running on Uvicorn"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}"}

@app.post("/items/")
async def create_item(item: Item):
    return {"item": item, "message": "Item created successfully"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "server": "uvicorn"}

if __name__ == "__main__":
    # Development mode
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug"
    )
```

### Run the application:

```bash
# Development
python main.py

# Or directly with uvicorn
uvicorn main:app --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Docker Deployment with Uvicorn

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### requirements.txt

```
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
```

### Build and Run

```bash
# Build image
docker build -t fastapi-uvicorn .

# Run container
docker run -d -p 8000:8000 --name myapi fastapi-uvicorn
```

---

## Performance Tuning

### 1. Worker Count Optimization

```bash
# For CPU-bound tasks
workers = CPU_cores

# For I/O-bound tasks (recommended for APIs)
workers = (2 × CPU_cores) + 1
```

### 2. Keep-Alive Settings

```bash
uvicorn main:app --timeout-keep-alive 5
```

Reduces connection overhead for clients making multiple requests.

### 3. Limit Request Size

```python
from fastapi import FastAPI

app = FastAPI()

# Limit request body size (16MB)
app.add_middleware(
    middleware_class=...,
    max_request_size=16 * 1024 * 1024
)
```

### 4. Enable HTTP/2 (via proxy)

Use Nginx or Traefik as reverse proxy for HTTP/2 support.

---

## Monitoring Uvicorn

### Access Logs

```bash
uvicorn main:app --access-log
```

Output:
```
INFO:     127.0.0.1:54321 - "GET / HTTP/1.1" 200 OK
INFO:     127.0.0.1:54322 - "POST /items/ HTTP/1.1" 201 Created
```

### Custom Logging

```python
import logging
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Run with custom log config
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config="log_config.yaml"
    )
```

---

## Common Issues and Solutions

### Issue 1: Port Already in Use

```bash
# Error: [Errno 98] Address already in use
# Solution: Change port or kill existing process
lsof -ti:8000 | xargs kill -9
```

### Issue 2: Workers Not Spawning

```bash
# Use Gunicorn for better worker management
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Issue 3: Slow Startup

```bash
# Disable reload in production
uvicorn main:app --no-reload
```

### Issue 4: Connection Timeout

```bash
# Increase timeout settings
uvicorn main:app --timeout-keep-alive 75
```

---

## Best Practices

1. **Development vs Production**
   - Development: Use `--reload` for auto-restart
   - Production: Use multiple workers, disable reload

2. **Use Gunicorn for Production**
   ```bash
   gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
   ```

3. **Behind Reverse Proxy**
   ```bash
   uvicorn main:app --proxy-headers --forwarded-allow-ips='*'
   ```

4. **Environment Variables**
   ```python
   import os
   port = int(os.getenv("PORT", 8000))
   uvicorn.run(app, host="0.0.0.0", port=port)
   ```

5. **Health Checks**
   ```python
   @app.get("/health")
   async def health():
       return {"status": "ok"}
   ```

---

## Summary

**Uvicorn** is the essential bridge between your FastAPI application and the outside world. It provides:

- ✅ High-performance ASGI server implementation
- ✅ Native async/await support for FastAPI
- ✅ Production-ready with proper configuration
- ✅ Simple development workflow with auto-reload
- ✅ Scalable with multi-worker support
- ✅ Compatible with process managers and containers

**Key Takeaway:** FastAPI defines *what* your API does, while Uvicorn handles *how* it serves requests to the world.

---

## Additional Resources

- [Uvicorn Documentation](https://www.uvicorn.org/)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [ASGI Specification](https://asgi.readthedocs.io/)
- [Performance Benchmarks](https://www.techempower.com/benchmarks/)
