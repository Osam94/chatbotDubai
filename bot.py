import os
import logging
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from pdf_parser import parse_pdf
from data_store import save_user_data, query_user_data

TOKEN = "7993767401:AAFeXQzNo74K2E5ZnkacbPJVLWKDNDMEjbU"
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"https://dubaibot-737q.onrender.com{WEBHOOK_PATH}"

app = Flask(__name__)
bot_app = ApplicationBuilder().token(TOKEN).concurrent_updates(True).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Отправь PDF файл, и я буду отвечать на запросы по нему. Чтобы заменить файл — просто отправь новый.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    file = await update.message.document.get_file()
    os.makedirs("user_files", exist_ok=True)
    pdf_path = f"user_files/{user_id}.pdf"
    await file.download_to_drive(pdf_path)
    df = parse_pdf(pdf_path)
    save_user_data(user_id, df)
    await update.message.reply_text("✅ PDF обработан. Теперь можешь задавать вопросы по артикулу, описанию и т.д.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    query = update.message.text.strip()
    response = query_user_data(user_id, query)
    await update.message.reply_markdown(response)

@app.route(WEBHOOK_PATH, methods=["POST"])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    asyncio.create_task(bot_app.process_update(update))
    return "OK"

async def setup():
    await bot_app.initialize()
    await bot_app.bot.delete_webhook()
    await bot_app.bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.Document.PDF, handle_document))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    asyncio.run(setup())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
