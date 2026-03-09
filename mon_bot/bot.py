import random
import logging
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# --- CONFIGURATION ---
TOKEN = "8745318621:AAGfnGlKFFBluDBrQpMhpekx54laLz..." # Ton Token Telegram
CODE_PROMO = "DIAO226" # Promo 1XBET, MELBET, 888STARZ

# --- FONCTION COULEURS ALÉATOIRES (EMOJIS) ---
def btn(text):
    colors = ["🔴", "🔵", "🟢", "🟡", "🟠", "🟣", "🟤", "⚪"]
    return f"{random.choice(colors)} {text}"

# --- GÉNÉRATEURS DE GRILLES (PRÉDICTIONS) ---
def get_prediction_text(game_name):
    if "Apple" in game_name:
        grid = "🍎 **APPLE OF FORTUNE**\n\n"
        for _ in range(6):
            row = ["⬛"] * 5
            row[random.randint(0, 4)] = "🍎"
            grid += "".join(row) + "\n"
        return grid
    elif "Crash" in game_name:
        cote = round(random.uniform(1.4, 9.5), 2)
        return f"🚀 **CRASH PREDICTION**\n\n📈 Montée en cours...\nCote cible : **{cote}x**"
    elif "Kamikaze" in game_name:
        grid = "✈️ **KAMIKAZE (AVIATOR)**\n\n"
        for _ in range(5):
            row = ["🟦"] * 5
            row[random.randint(0, 4)] = "✈️"
            grid += "".join(row) + "\n"
        return grid
    elif "Mines" in game_name:
        grid = "💎 **GEMS AND MINES**\n\n"
        for _ in range(5):
            row = ["⬛"] * 5
            row[random.randint(0, 4)] = "💎"
            grid += "".join(row) + "\n"
        return grid
    elif "Thimbles" in game_name:
        pos = random.randint(1, 3)
        res = ["💡", "💡", "💡"]
        res[pos-1] = "💎"
        return f"🎲 **THIMBLES**\n\nPosition : **{pos}**\n{' '.join(res)}"
    elif "Under" in game_name:
        res = random.choice(["Moins de 7 (Under)", "Plus de 7 (Over)", "Égal à 7"])
        return f"🎲 **UNDER AND OVER 7**\n\nRésultat : **{res}**"
    return "🎰 Analyse en cours..."

# --- GESTION DES COMMANDES ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    context.user_data['streak'] = 0 # Reset du compteur vocal
    
    # Menu Principal (3 Boutons)
    keyboard = [
        [btn("Menu Jeux 🎮")],
        [btn("Question ❓"), btn("Retour ⬅️")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        f"Salut {user_name} ! 👋\n\n"
        f"Bienvenue sur ton bot de prédiction **1XBET, MELBET & 888STARZ**.\n"
        f"Veuillez saisir l'ID de votre compte créé avec le Code Promo : `{CODE_PROMO}`",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_data = context.user_data
    
    # 1. Navigation : Menu Jeux
    if "Menu Jeux" in text:
        keyboard = [
            [btn("Apple Of Fortune"), btn("Crash")],
            [btn("Kamikaze"), btn("Gems And Mines")],
            [btn("Thimbles"), btn("Under And Over7")],
            [btn("Retour ⬅️")]
        ]
        await update.message.reply_text(
            "🕹️ **SÉLECTIONNEZ VOTRE JEU :**",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
            parse_mode='Markdown'
        )

    # 2. Navigation : Retour
    elif "Retour" in text:
        await start(update, context)

    # 3. Navigation : Question
    elif "Question" in text:
        await update.message.reply_text(
            "❓ **AIDE & MODE D'EMPLOI**\n\n"
            f"1. Créez un compte Melbet ou 888Starz avec le code `{CODE_PROMO}`.\n"
            "2. Déposez au moins 2000 FCFA.\n"
            "3. Choisissez un jeu et suivez les prédictions illimitées du bot.",
            parse_mode='Markdown'
        )

    # 4. Logique des Jeux & Vocal
    elif any(game in text for game in ["Apple", "Crash", "Kamikaze", "Gems", "Thimbles", "Under"]):
        # Envoi de la prédiction
        prediction = get_prediction_text(text)
        footer = f"\n\n👉 **Code Promo: {CODE_PROMO}**"
        await update.message.reply_text(prediction + footer, parse_mode='Markdown')
        
        # Gestion du Vocal (Toutes les 3 prédictions)
        user_data['streak'] = user_data.get('streak', 0) + 1
        if user_data['streak'] >= 3:
            user_data['streak'] = 0
            try:
                with open('ma_voix_off.mp3', 'rb') as voice_file:
                    await update.message.reply_voice(
                        voice=voice_file,
                        caption="🎙️ **CONSEIL DE L'EXPERT**"
                    )
            except FileNotFoundError:
                pass # Si le fichier n'est pas là, le bot continue sans erreur

# --- LANCEMENT ---
if __name__ == '__main__':
    print("Bot en ligne...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
