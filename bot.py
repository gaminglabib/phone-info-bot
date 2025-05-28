import logging
import aiohttp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "7921673777:AAH5GqPcew87tpTJQNwpQEt24gkld-QiEg0"
NUMVERIFY_API_KEY = "09f5db7c22b7491c8f92ba7c87d619cb"  # তোমার API কী

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"প্রিয় {user.first_name}, নম্বর ইনফো বটে স্বাগতম!\n"
        "তুমি /phone <number> কমান্ড দিয়ে ফোন নম্বরের তথ্য পেতে পারবে।\n"
        "উদাহরণ: /phone 01712345678"
    )

async def phone_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("দয়া করে একটি ফোন নম্বর লিখুন।\nউদাহরণ: /phone 01712345678")
        return

    phone_number = context.args[0]

    url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={phone_number}&country_code=BD&format=1"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("valid"):
                        response_message = f"নম্বর: {phone_number}\n"
                        response_message += f"দেশ: {data.get('country_name', 'তথ্য নেই')}\n"
                        response_message += f"অপারেটর: {data.get('carrier', 'তথ্য নেই')}\n"
                        response_message += f"লোকেশন: {data.get('location', 'তথ্য নেই')}\n"
                        response_message += f"টাইপ: {data.get('line_type', 'তথ্য নেই')}\n"
                        await update.message.reply_text(response_message)
                    else:
                        await update.message.reply_text("দুঃখিত, নম্বরটি সঠিক নয় বা তথ্য পাওয়া যায়নি।")
                else:
                    await update.message.reply_text("সার্ভার থেকে তথ্য আনা যায়নি। পরে চেষ্টা করুন।")
    except Exception as e:
        logger.error(f"Error fetching phone info: {e}")
        await update.message.reply_text("সার্ভারে সমস্যা হয়েছে, পরে আবার চেষ্টা করুন।")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("phone", phone_info))

    print("Bot started...")
    app.run_polling()
