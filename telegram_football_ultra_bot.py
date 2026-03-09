# ===============================
# FOOTBALL ULTRA BOT – TERMUX SAFE
# ===============================

import logging
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# ========= CONFIG =========
BOT_TOKEN = "8492947598:AAH7fk_W8mtjfQL4m7BtNeOJbcDCtqISyHU"
API_FOOTBALL_KEY = "bbf2ec9682b0879d3f078328952bc61e"
CHANNEL_ID = 1003665113617   # ID du canal

API_HEADERS = {
    "x-apisports-key": API_FOOTBALL_KEY
}

LANG = "fr"  # fr / en

# ========= LOG =========
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ========= TEXT =========
TEXT = {
    "fr": {
        "start": "⚽ Bot Football ULTRA actif",
        "manual": "📢 Publication manuelle envoyée",
        "today": "📅 Matchs du jour"
    },
    "en": {
        "start": "⚽ Football ULTRA Bot active",
        "manual": "📢 Manual post sent",
        "today": "📅 Today's matches"
    }
}

# ========= IMAGE SCORE =========
def generate_score_image(home, away, score):
    img = Image.new("RGB", (800, 400), "#0b132b")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/system/fonts/Roboto-Regular.ttf", 48)
    except:
        font = ImageFont.load_default()

    draw.text((50, 150), home, fill="white", font=font)
    draw.text((350, 150), score, fill="yellow", font=font)
    draw.text((600, 150), away, fill="white", font=font)

    path = "score.png"
    img.save(path)
    return path

# ========= API =========
def get_today_matches():
    today = datetime.now().strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?date={today}"
    r = requests.get(url, headers=API_HEADERS)
    return r.json()["response"]

# ========= COMMANDS =========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TEXT[LANG]["start"])

async def send_manual(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await publish_today(context)
    await update.message.reply_text(TEXT[LANG]["manual"])

# ========= PUBLISH =========
async def publish_today(context: ContextTypes.DEFAULT_TYPE):
    matches = get_today_matches()

    for m in matches[:10]:
        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]
        goals_h = m["goals"]["home"]
        goals_a = m["goals"]["away"]
        score = f"{goals_h} - {goals_a}"

        img = generate_score_image(home, away, score)

        await context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=open(img, "rb"),
            caption=f"⚽ {home} {score} {away}"
        )

# ========= MAIN =========
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("send", send_manual))

    print("🔥 FOOTBALL ULTRA BOT – ACTIF")
    app.run_polling()

if __name__ == "__main__":
    main()
