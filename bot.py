import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from pdf_parser import parse_pdf
from data_store import load_data, query_data

# Hardcoded token (for Render environment without .env support)
TOKEN = "7993767401:AAFeXQzNo74K2E5ZnkacbPJVLWKDNDMEjbU"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне PDF-файл, и я буду отвечать на запросы по нему.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    file_path = "latest.pdf"
    await file.download_to_drive(file_path)
    df = parse_pdf(file_path)
    load_data(df)
    await update.message.reply_text("PDF загружен и обработан. Можешь отправлять запросы по артикулу, описанию, номеру отправления и т.д.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    if "заменить" in query.lower() and "pdf" in query.lower():
        await update.message.reply_text("Ок, отправь новый PDF.")
    else:
        result = query_data(query)
        await update.message.reply_markdown(result)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("Бот запущен...")
    app.run_polling()
