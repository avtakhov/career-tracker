FROM python:3.10

WORKDIR /app

COPY . /app

RUN chmod +x ./start.sh
RUN pip install .


RUN useradd --create-home appuser
USER appuser

ENV ENVIRONMENT=${ENVIRONMENT}
ENV WEBHOOK_URL=${WEBHOOK_URL}
ENV TELEGRAM_TOKEN=${TELEGRAM_TOKEN}

CMD ["./start.sh"]
