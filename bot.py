import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import aiohttp

# তোমার বট টোকেন এখানে বসাও
BOT_TOKEN = "7921673777:AAH5GqPcew87tpTJQNwpQEt24gkld-QiEg0"

# Render এ তোমার ডিপ্লয় করা URL (https://phone-info-bot.onrender.com)
RENDER_URL = "https://phone-info-bot.onrender.com"

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
        "উদাহরণ: /phone 01712345678"
    )

async def phone_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("দয়া করে একটি ফোন নম্বর সরাসরি লিখো।\nউদাহরণ: /phone 01712345678")
        return
    
    phone_number = context.args[0]
    await update.message.reply_text(f"{phone_number} নম্বরের তথ্য খুঁজছি...")

    try:
        async with aiohttp.ClientSession() as session:
            # এখানে তোমার Render URL দিয়ে GET রিকোয়েস্ট পাঠানো হবে
            async with session.get(f"{RENDER_URL}/api/phoneinfo?number={phone_number}") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    # ধরে নিচ্ছি API থেকে JSON ডাটা আসবে, তুমি প্রাসঙ্গিক অংশ এখানে ফরম্যাট করে পাঠাতে পারো
                    response_message = f"নম্বর: {phone_number}\n"
                    response_message += f"দেশ: {data.get('country', 'তথ্য নেই')}\n"
                    response_message += f"অপারেটর: {data.get('operator', 'তথ্য নেই')}\n"
                    response_message += f"অঞ্চল: {data.get('region', 'তথ্য নেই')}\n"
                    await update.message.reply_text(response_message)
                else:
                    await update.message.reply_text("দুঃখিত, নম্বরের তথ্য পাওয়া যায়নি।")
    except Exception as e:
        logger.error(f"Error fetching phone info: {e}")
        await update.message.reply_text("দুঃখিত, সার্ভারে সমস্যা হয়েছে। পরে আবার চেষ্টা করুন।")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # এই ফাংশন দিয়ে বট নিজে নিজে পং করে কাজ করছে কিনা চেক করবে
    await update.message.reply_text("Pong! বট সচল আছে।")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("phone", phone_info))
    app.add_handler(CommandHandler("ping", ping))

    print("Bot started...")
    app.run_polling()
