FROM python:3.15-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libxcb1 \
        libgl1 \
        libxext6 \
        libx11-6 \
        libsm6 \
        libice6 \
        libglib2.0-0t64 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /ml-client
RUN pip install --no-cache-dir pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy
COPY . .
EXPOSE 6700
CMD ["python", "client.py"]