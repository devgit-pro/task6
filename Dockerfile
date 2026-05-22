FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM gcr.io/distroless/python3-debian12:nonroot

WORKDIR /app

ENV PYTHONPATH=/usr/local/lib/python3.12/site-packages
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY --from=builder /install /usr/local
COPY app/ /app/

USER nonroot:nonroot

EXPOSE 5000

CMD ["-m", "gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "30", "app:app"]
