import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import aiohttp

# তোমার বট টোকেন এখানে বসাও
BOT_TOKEN = "7921673777:AAH5GqPcew87tpTJQNwpQEt24gkld-QiEg0"

# তোমার numverify API key এখানে বসাও
API_KEY = "09f5db7c22b7491c8f92ba7c87d619cb"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"প্রিয় {user.first_name}, Toxic Digonto এর বট-এ আপনাকে স্বাগতম।\n"
        "আমি তোমার ফোন নম্বর ইনফো দিয়ে সাহায্য করব।\n"
        "তুমি /phone <number> কমান্ড দিয়ে নম্বরের তথ্য জানতে পারবে।\n"
        "উদাহরণ: /phone +8801712345678\n\n"
        "দয়া করে অবশ্যই আন্তর্জাতিক ফরম্যাটে নম্বর পাঠাও।"
    )

async def phone_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text(
            "দয়া করে একটি ফোন নম্বর সরাসরি লিখো আন্তর্জাতিক ফরম্যাটে।\n"
            "উদাহরণ: /phone +8801712345678"
        )
        return

    phone_number = context.args[0]

    # নম্বর অবশ্যই + দিয়ে শুরু হচ্ছে কিনা চেক
    if not phone_number.startswith("+"):
        await update.message.reply_text(
            "দুঃখিত, নম্বরটি আন্তর্জাতিক ফরম্যাটে হতে হবে।\n"
            "যেমন: +8801712345678"
        )
        return

    await update.message.reply_text(f"{phone_number} নম্বরের তথ্য খুঁজছি...")

    url = f"http://apilayer.net/api/validate?access_key={API_KEY}&number={phone_number}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()

                    if data.get("valid"):
                        country = data.get("country_name", "তথ্য নেই")
                        location = data.get("location", "তথ্য নেই")
                        carrier = data.get("carrier", "তথ্য নেই")
                        line_type = data.get("line_type", "তথ্য নেই")

                        response_message = (
                            f"📞 নম্বর: {phone_number}\n"
                            f"🌍 দেশ: {country}\n"
                            f"📌 লোকেশন: {location}\n"
                            f"📡 অপারেটর: {carrier}\n"
                            f"📱 টাইপ: {line_type}"
                        )
                        await update.message.reply_text(response_message)
                    else:
                        await update.message.reply_text("দুঃখিত, নম্বরটি সঠিক নয় অথবা তথ্য পাওয়া যায়নি।")
                else:
                    await update.message.reply_text("⚠️ সার্ভার থেকে তথ্য আনা যায়নি। পরে আবার চেষ্টা করুন।")
    except Exception as e:
        logger.error(f"Error fetching phone info: {e}")
        await update.message.reply_text("দুঃখিত, সার্ভারে সমস্যা হয়েছে। পরে আবার চেষ্টা করুন।")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong! বট সচল আছে।")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("phone", phone_info))
    app.add_handler(CommandHandler("ping", ping))

    print("Bot started...")
    app.run_polling()
