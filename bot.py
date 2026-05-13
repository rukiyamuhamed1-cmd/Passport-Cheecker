import os
import fitz  # PyMuPDF
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

# PDF text save
pdf_text = ""


# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "PDF Ergi.\n"
        "PDF erga upload  booda maqaa barreessi."
    )


# PDF RECEIVE
async def receive_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global pdf_text

    document = update.message.document

    if not document.file_name.lower().endswith(".pdf"):
        await update.message.reply_text("PDF file qofa ergi.")
        return

    file = await context.bot.get_file(document.file_id)

    os.makedirs("downloads", exist_ok=True)

    file_path = f"downloads/{document.file_name}"

    await file.download_to_drive(file_path)

    try:
        text = ""
        pdf = fitz.open(file_path)

        for page in pdf:
            text += page.get_text()

        pdf.close()

        pdf_text = text.lower()

        await update.message.reply_text(
            "PDF Milkaa'inaan Galmaa'e. Amma maqaa ergi."
        )

    except Exception as e:
        await update.message.reply_text(f"Dogoggora: {e}")


# SEARCH NAME
async def search_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global pdf_text

    if pdf_text == "":
        await update.message.reply_text(
            "Dura PDF ergi."
        )
        return

    name = update.message.text.strip().lower()

    if name in pdf_text:
        await update.message.reply_text(
            "Bagaa Gammadan Passportiin Kessan Baheraa."
        )
    else:
        await update.message.reply_text(
            "Maaloo Paasportiin Kessan bahe hin jiru obsan Eegadhaa."
        )


# MAIN

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(filters.Document.PDF, receive_pdf)
    )

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, search_name)
    )

    print("Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()