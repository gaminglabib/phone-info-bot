import logging
import aiohttp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ✅ তোমার বট টোকেন এখানে বসাও
BOT_TOKEN = "7921673777:AAH5GqPcew87tpTJQNwpQEt24gkld-QiEg0"

# ✅ ফ্রি API ইউআরএল (numverify demo API)
API_KEY = "e6d5e63c2cfd316ae203d62c6cc07d8e"  # demo key
API_URL = "http://apilayer.net/api/validate"

# ✅ লগ সেটআপ
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ✅ /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"প্রিয় {user.first_name}, Toxic Digonto এর বট-এ আপনাকে স্বাগতম।\n"
        "আমি তোমার ফোন নম্বর ইনফো দিয়ে সাহায্য করব।\n"
        "তুমি /phone <number> কমান্ড দিয়ে নম্বরের তথ্য জানতে পারবে।\n"
        "উদাহরণ: /phone +8801712345678"
    )

# ✅ /phone কমান্ড
async def phone_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("দয়া করে একটি ফোন নম্বর সরাসরি লিখো।\nউদাহরণ: /phone +8801712345678")
        return

    phone_number = context.args[0]
    await update.message.reply_text(f"{phone_number} নম্বরের তথ্য খুঁজছি...")

    try:
        async with aiohttp.ClientSession() as session:
            params = {
                "access_key": API_KEY,
                "number": phone_number,
                "format": 1
            }
            async with session.get(API_URL, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("valid"):
                        response_message = f"📱 নম্বর: {data.get('international_format', phone_number)}\n"
                        response_message += f"🌍 দেশ: {data.get('country_name', 'তথ্য নেই')}\n"
                        response_message += f"📞 কোড: +{data.get('country_code', '')}\n"
                        response_message += f"📡 ক্যারিয়ার: {data.get('carrier', 'তথ্য নেই')}\n"
                        response_message += f"🛰️ লাইন টাইপ: {data.get('line_type', 'তথ্য নেই')}"
                        await update.message.reply_text(response_message)
                    else:
                        await update.message.reply_text("দুঃখিত, নম্বরটি সঠিক নয় অথবা তথ্য পাওয়া যায়নি।")
                else:
                    await update.message.reply_text("দুঃখিত, সার্ভার থেকে তথ্য আনতে সমস্যা হয়েছে।")
    except Exception as e:
        logger.error(f"Error fetching phone info: {e}")
        await update.message.reply_text("দুঃখিত, কিছু একটা ভুল হয়েছে। পরে আবার চেষ্টা করুন।")

# ✅ /ping কমান্ড
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Pong! বট সচল আছে।")

# ✅ main runner
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("phone", phone_info))
    app.add_handler(CommandHandler("ping", ping))

    print("✅ Bot started...")
    app.run_polling()
