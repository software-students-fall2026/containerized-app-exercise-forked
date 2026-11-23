FROM python:3.15-slim
WORKDIR /ml-client
RUN pip install --no-cache-dir pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy
COPY . .
EXPOSE 6700
CMD ["python", "client.py"]