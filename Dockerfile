FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/
# Install Python dependencies (aiogram 2.x and dotenv)
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "bot.py"]
