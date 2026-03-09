import os
import asyncio
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# ================= LOAD ENV =================
load_dotenv()

BOT_TOKEN = os.getenv("8492947598:AAH7fk_W8mtjfQL4m7BtNeOJbcDCtqISyHU")
CHANNEL_ID = -1003665113617
API_KEY = os.getenv("bbf2ec9682b0879d3f078328952bc61e")

API_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}

posted_goals = set()

# ================= COMMANDS =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚽ FOOTBALL ULTRA BOT\n"
        "📺 Niveau TV Sport\n"
        "🔴 Live matchs réels activés"
    )

# ================= MATCHS DU JOUR =================
async def matchs_du_jour(context: ContextTypes.DEFAULT_TYPE):
    params = {"date": asyncio.get_event_loop().time().__class__.__name__}
    params = {"date": __import__("datetime").date.today().isoformat()}

    r = requests.get(f"{API_URL}/fixtures", headers=HEADERS, params=params)
    data = r.json()["response"]

    if not data:
        return

    msg = "📅 MATCHS DU JOUR\n\n"
    for m in data[:5]:
        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]
        time = m["fixture"]["date"][11:16]
        msg += f"⚽ {home} vs {away}\n⏰ {time}\n\n"

    await context.bot.send_message(chat_id=CHANNEL_ID, text=msg)

# ================= LIVE JOB =================
async def live_job(context: ContextTypes.DEFAULT_TYPE):
    params = {"live": "all"}
    r = requests.get(f"{API_URL}/fixtures", headers=HEADERS, params=params)
    data = r.json()["response"]

    for m in data:
        fixture_id = m["fixture"]["id"]
        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        for g in m["events"]:
            if g["type"] == "Goal":
                uid = f"{fixture_id}-{g['time']['elapsed']}-{g['player']['name']}"
                if uid not in posted_goals:
                    posted_goals.add(uid)

                    score = f"{m['goals']['home']} - {m['goals']['away']}"

                    msg = (
                        f"⚽ BUT !!!\n"
                        f"{home} vs {away}\n"
                        f"👤 {g['player']['name']}\n"
                        f"⏱ {g['time']['elapsed']}'\n"
                        f"📊 Score : {score}"
                    )

                    await context.bot.send_message(chat_id=CHANNEL_ID, text=msg)

# ================= MAIN =================
async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.job_queue.run_once(matchs_du_jour, when=5)
    app.job_queue.run_repeating(live_job, interval=60, first=10)

    print("✅ FOOTBALL ULTRA BOT – API-FOOTBALL LIVE ACTIF")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
