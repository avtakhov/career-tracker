FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install .

EXPOSE 8000

RUN useradd --create-home appuser
USER appuser

# CMD with JSON notation
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
