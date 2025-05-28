import logging
import aiohttp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "7921673777:AAH5GqPcew87tpTJQNwpQEt24gkld-QiEg0"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "https://api.apilayer.com/number_verification/validate?number={number}"
API_KEY = "e1d3d0a7e6msh6c928643e3b79d6p1c85fajsnc86d8fd50c92"  # Demo key

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"প্রিয় {user.full_name}, Toxic Digonto এর বট-এ আপনাকে স্বাগতম।\n\n"
        "📞 আপনি /phone <নম্বর> লিখে ফোন নম্বরের তথ্য জানতে পারবেন।\n"
        "উদাহরণ: /phone +8801712345678"
    )

async def phone_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("❗ দয়া করে একটি সঠিক ফোন নম্বর লিখুন।\nযেমন: /phone +8801712345678")
        return
    
    number = context.args[0]
    await update.message.reply_text(f"🔍 {number} নম্বরের তথ্য খুঁজছি...")

    headers = {
        "apikey": API_KEY
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL.format(number=number), headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                if data.get("valid"):
                    response = (
                        f"✅ তথ্য পাওয়া গেছে:\n"
                        f"📞 নম্বর: {data.get('international_format', number)}\n"
                        f"🌍 দেশ: {data.get('country_name', 'নেই')}\n"
                        f"📱 অপারেটর: {data.get('carrier', 'নেই')}\n"
                        f"📶 লাইন টাইপ: {data.get('line_type', 'নেই')}"
                    )
                    await update.message.reply_text(response)
                else:
                    await update.message.reply_text("❌ দুঃখিত, নম্বরটি সঠিক নয় অথবা তথ্য পাওয়া যায়নি।")
            else:
                await update.message.reply_text("⚠️ সার্ভার থেকে তথ্য আনা যায়নি। পরে আবার চেষ্টা করুন।")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("phone", phone_info))

    print("📡 Bot is running...")
    app.run_polling()
