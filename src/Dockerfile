FROM python:3.11


WORKDIR /app

COPY . .

RUN pip install -r requirements.txt --no-cache-dir


CMD ["uvicorn", "core.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
