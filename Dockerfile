FROM python:3.10

WORKDIR /app

COPY . /app
COPY . /env
COPY . /start.sh

RUN pip install .

RUN useradd --create-home appuser
USER appuser

ENV ENVIRONMENT=${ENVIRONMENT}

CMD ["./start.sh"]
