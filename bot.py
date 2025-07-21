import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from aiogram.utils import executor
from dotenv import load_dotenv

from bot_utils import load_posts, append_log, update_subscription

load_dotenv("config/bot.env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
GOOGLE_DRIVE_URL = os.getenv("GOOGLE_DRIVE_URL")
DELAY_BETWEEN_POSTS = int(os.getenv("DELAY_BETWEEN_POSTS", "10"))
LOG_FILE = os.getenv("LOG_FILE", "stats.csv")
POSTS_JSON = os.getenv("POSTS_JSON", "config/posts.json")
MEDIA_FOLDER = os.getenv("MEDIA_FOLDER", "media/")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


async def send_posts(chat_id: int):
    posts = load_posts(POSTS_JSON)
    for post in posts:
        for media in post.get("media", []):
            path = os.path.join(MEDIA_FOLDER, media)
            ext = os.path.splitext(media)[1].lower()
            if ext in {".jpg", ".jpeg", ".png"}:
                await bot.send_photo(chat_id, InputFile(path))
            elif ext == ".gif":
                await bot.send_animation(chat_id, InputFile(path))
            elif ext in {".mov", ".mp4"}:
                await bot.send_video(chat_id, InputFile(path))
        await bot.send_message(chat_id, post["text"], parse_mode="Markdown")
        await asyncio.sleep(DELAY_BETWEEN_POSTS)


async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
    except Exception:
        return False
    return member.status in {"member", "creator", "administrator"}


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    """Show the initial \"Начать\" button."""
    button = InlineKeyboardButton("▶️ Начать", callback_data="start_posts")
    markup = InlineKeyboardMarkup().add(button)
    await message.answer(
        "Нажмите «Начать», чтобы получить статью и серию постов", reply_markup=markup
    )


@dp.callback_query_handler(lambda c: c.data == "start_posts")
async def process_start(callback_query: types.CallbackQuery):
    """Send greeting, posts and final button when user presses start."""
    await callback_query.answer()
    chat_id = callback_query.message.chat.id
    user = callback_query.from_user

    append_log(LOG_FILE, user)
    greeting = (
        f"{user.first_name}, лови статью «Чек‑ап женского здоровья: как не пропустить "
        f"важное и сохранить молодость?»\n\n{GOOGLE_DRIVE_URL}"
    )
    await bot.send_message(chat_id, greeting, parse_mode="Markdown")

    await send_posts(chat_id)
    subscribed = await check_subscription(user.id)
    if subscribed:
        text = "Перейти в канал:"
        button_text = "➡️ Перейти в канал"
    else:
        text = "Подпишись на канал, чтобы не пропустить важное!"
        button_text = "🔔 Подписаться на канал"

    button = InlineKeyboardButton(
        button_text, url=f'https://t.me/{CHANNEL_USERNAME.lstrip("@")}'
    )
    markup = InlineKeyboardMarkup().add(button)
    await bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")
    update_subscription(LOG_FILE, user.id, "yes" if subscribed else "no")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
