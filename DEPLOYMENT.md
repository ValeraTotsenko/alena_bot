# Deploying Alena Bot

These steps describe how to launch the bot on your server.

1. **Clone the repository**

```bash
git clone <repo-url> alena_bot
cd alena_bot
```

2. **Create the environment file**

Copy the example file and fill in your values:

```bash
cp config/bot.env.example config/bot.env
# edit config/bot.env with your BOT_TOKEN and other settings
```

This file is listed in `.gitignore`, so your credentials will not be committed to the repository.

3. **Create a Python virtual environment and install dependencies**

```bash
python3 -m venv venv
source venv/bin/activate
 pip install aiogram==2.25.1 python-dotenv
```

4. **Run the bot**

```bash
python bot.py
```

Alternatively, you can use Docker:

```bash
docker-compose up -d
```

Or install the `alena_bot.service` unit and start it via systemd.

