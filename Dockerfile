FROM python:3.11-slim-bookworm

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root \
    && pip uninstall poetry -y

COPY . .

CMD ["python", "main.py"]