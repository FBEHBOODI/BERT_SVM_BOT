import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from transformers import pipeline

# بارگذاری مدل BERT آماده از Hugging Face
bert_pipe = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# توکن بات تلگرام را از متغیر محیطی بگیر
TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! یک جمله بفرست تا تحلیل احساسات انجام بدم (با مدل BERT).")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    result = bert_pipe(text)[0]
    label = result['label']
    score = round(result['score'] * 100, 2)
    response = f"نتیجه تحلیل احساسات:
برچسب: {label}
درصد اطمینان: {score}%"
    await update.message.reply_text(response)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
