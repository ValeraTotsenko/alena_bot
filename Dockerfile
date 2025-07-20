FROM python:3.11-slim

WORKDIR /app

COPY . /app

# Pin aiogram 2.x to match the bot source code
RUN pip install --no-cache-dir aiogram==2.25.1 python-dotenv

CMD ["python", "bot.py"]
