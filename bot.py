import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.constants import ParseMode
from sherlock_core import cerca_username

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "INSERISCI_QUI_IL_TUO_TOKEN"
WATERMARK = "\n\n🔍 *By Drain* | @fattissimo"

# ── /start ──────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔍 Cerca username", callback_data="cerca")],
        [InlineKeyboardButton("ℹ️ Come funziona", callback_data="info")],
        [InlineKeyboardButton("📊 Piattaforme supportate", callback_data="piattaforme")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    testo = (
        "👁️ *DRAIN OSINT BOT*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Trova profili pubblici su oltre *300+ piattaforme*"
        " partendo da un semplice username.\n\n"
        "Scrivi `/cerca <username>` oppure usa il bottone qui sotto."
        + WATERMARK
    )
    await update.message.reply_text(testo, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)

# ── callback bottoni ─────────────────────────────────────────────────────────
async def bottone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "cerca":
        await query.edit_message_text(
            "✏️ *Inviami l'username* da cercare.\n\nEsempio: `mario_rossi`" + WATERMARK,
            parse_mode=ParseMode.MARKDOWN,
        )
        context.user_data["aspetta_username"] = True

    elif query.data == "info":
        testo = (
            "ℹ️ *Come funziona Drain OSINT Bot*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "1️⃣ Inserisci un username\n"
            "2️⃣ Il bot controlla automaticamente centinaia di siti\n"
            "3️⃣ Ricevi la lista dei profili trovati con i link diretti\n\n"
            "⚠️ *Nota:* vengono controllati solo URL pubblicamente accessibili. "
            "Nessuna password, nessun dato privato."
            + WATERMARK
        )
        keyboard = [[InlineKeyboardButton("🔙 Torna indietro", callback_data="start")]]
        await query.edit_message_text(testo, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "piattaforme":
        testo = (
            "📊 *Piattaforme principali controllate*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Instagram • TikTok • Twitter/X • YouTube\n"
            "GitHub • GitLab • Reddit • Pinterest\n"
            "LinkedIn • Twitch • SoundCloud • Spotify\n"
            "Telegram • Discord • Steam • Snapchat\n"
            "Tumblr • Medium • Flickr • DeviantArt\n\n"
            "_...e altri 280+ siti internazionali_"
            + WATERMARK
        )
        keyboard = [[InlineKeyboardButton("🔙 Torna indietro", callback_data="start")]]
        await query.edit_message_text(testo, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "start":
        keyboard = [
            [InlineKeyboardButton("🔍 Cerca username", callback_data="cerca")],
            [InlineKeyboardButton("ℹ️ Come funziona", callback_data="info")],
            [InlineKeyboardButton("📊 Piattaforme supportate", callback_data="piattaforme")],
        ]
        testo = (
            "👁️ *DRAIN OSINT BOT*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Trova profili pubblici su oltre *300+ piattaforme*"
            " partendo da un semplice username.\n\n"
            "Scrivi `/cerca <username>` oppure usa il bottone qui sotto."
            + WATERMARK
        )
        await query.edit_message_text(testo, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(keyboard))

# ── /cerca <username> ────────────────────────────────────────────────────────
async def cerca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ Specifica un username!\n\nEsempio: `/cerca mario_rossi`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return
    username = context.args[0].strip()
    await avvia_ricerca(update, context, username)

# ── gestione messaggi liberi (dopo bottone "cerca") ──────────────────────────
async def messaggio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("aspetta_username"):
        context.user_data["aspetta_username"] = False
        username = update.message.text.strip()
        await avvia_ricerca(update, context, username)
    else:
        await update.message.reply_text(
            "Usa /cerca <username> oppure /start per il menu principale.",
            parse_mode=ParseMode.MARKDOWN,
        )

# ── logica ricerca ───────────────────────────────────────────────────────────
async def avvia_ricerca(update: Update, context: ContextTypes.DEFAULT_TYPE, username: str):
    msg = await update.message.reply_text(
        f"⏳ Ricerca in corso per `{username}`...\n_Controllo 300+ piattaforme, attendi._",
        parse_mode=ParseMode.MARKDOWN,
    )

    loop = asyncio.get_event_loop()
    trovati, errori = await loop.run_in_executor(None, cerca_username, username)

    if not trovati:
        await msg.edit_text(
            f"😶 Nessun profilo trovato per `{username}`.\n\n"
            "Prova con una variante del nome (es. con punto o trattino)." + WATERMARK,
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    # Suddivide i risultati in blocchi da max 4096 caratteri
    header = (
        f"✅ *Profili trovati per `{username}`*\n"
        f"📌 *{len(trovati)} risultati* su {len(trovati) + errori} siti\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
    )
    righe = [f"• [{sito}]({url})" for sito, url in trovati]
    footer = WATERMARK

    blocchi = []
    corrente = header
    for riga in righe:
        if len(corrente) + len(riga) + 1 > 4000:
            blocchi.append(corrente)
            corrente = ""
        corrente += riga + "\n"
    corrente += footer
    blocchi.append(corrente)

    await msg.edit_text(blocchi[0], parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    for blocco in blocchi[1:]:
        await update.message.reply_text(blocco, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

# ── avvio ────────────────────────────────────────────────────────────────────
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cerca", cerca))
    app.add_handler(CallbackQueryHandler(bottone))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messaggio))
    logger.info("Bot avviato!")
    app.run_polling()

if __name__ == "__main__":
    main()
