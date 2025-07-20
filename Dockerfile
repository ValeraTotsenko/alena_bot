FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir aiogram python-dotenv

CMD ["python", "bot.py"]
