TOKEN = "8492947598:AAH7fk_W8mtjfQL4m7BtNeOJbcDCtqISyHU"
‎CANAL_ID = -1003665892803
‎
‎MESSAGES_MATIN = [
‎    "🌅 Bonjour la famille 💙\nAujourd’hui on encaisse plus qu’hier 💪🔥",
‎    "☀️ Bon réveil à tous 👊\nDiscipline et patience, le gain arrive 💰",
‎    "🌄 Nouveau jour = nouvelle chance\nOn vise le vert aujourd’hui ✅"
‎]
‎
‎MESSAGES_SOIR = [
‎    "🌆 Bonsoir l’équipe 👊\nComment sont les coupons aujourd’hui ?",
‎    "📊 Petit point du jour\nÇa gagne ou ça résiste aujourd’hui ?",
‎    "🌇 La famille, dites-nous\nLes coupons sont comment aujourd’hui ?"
‎]
‎
‎MESSAGES_NUIT = [
‎    "🌙 Bonne nuit la famille 🤍",
‎    "😴 Bonne nuit à tous",
‎    "🌌 Bonne nuit, reposez-vous bien",
‎    "🙏 Bonne nuit, demain on revient plus forts"
‎]
‎
‎async def message_matin(context: ContextTypes.DEFAULT_TYPE):
‎    await context.bot.send_message(
‎        chat_id=CANAL_ID,
‎        text=random.choice(MESSAGES_MATIN)
‎    )
‎
‎async def message_soir(context: ContextTypes.DEFAULT_TYPE):
‎    await context.bot.send_message(
‎        chat_id=CANAL_ID,
‎        text=random.choice(MESSAGES_SOIR)
‎    )
‎
‎async def message_nuit(context: ContextTypes.DEFAULT_TYPE):
‎    await context.bot.send_message(
‎        chat_id=CANAL_ID,
‎        text=random.choice(MESSAGES_NUIT)
‎    )
‎
‎app = ApplicationBuilder().token(TOKEN).build()
‎job_queue = app.job_queue
‎
‎job_queue.run_daily(message_matin, time(hour=7, minute=0))
‎job_queue.run_daily(message_soir, time(hour=17, minute=0))
‎job_queue.run_daily(message_nuit, time(hour=0, minute=55))
‎
‎print("🤖 Bot automatique lancé...")
‎app.run_polling()
‎EOF
