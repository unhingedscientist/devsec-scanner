# Multi-stage Dockerfile for DevSec Scanner
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . .
RUN useradd -m scanner && chown -R scanner /app
USER scanner
EXPOSE 8080
HEALTHCHECK CMD ["python", "-c", "import sys; sys.exit(0)"]
ENTRYPOINT ["python", "main_cli.py"]
