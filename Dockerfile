FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN echo 'asdfadsf'
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

