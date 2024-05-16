FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install .

RUN useradd --create-home appuser
USER appuser

ENV ENVIRONMENT=${ENVIRONMENT}

CMD ["/app/start.sh"]
