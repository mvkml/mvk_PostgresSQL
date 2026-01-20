FROM python:3.11-slim

WORKDIR /code

# OS dependencies needed for pyodbc runtime (provides libodbc.so.2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc unixodbc-dev \
    curl ca-certificates \
    gcc g++ \
 && rm -rf /var/lib/apt/lists/*

# Python deps
COPY app/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# App code
COPY ./app /code/app

EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
