FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

RUN apt update \
    && apt install -y bash git gcc g++ make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

