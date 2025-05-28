import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import httpx

# 🔐 তোমার বট টোকেন এখানে বসাও
BOT_TOKEN = "7921673777:AAH5GqPcew87tpTJQNwpQEt24gkld-QiEg0"

# ✅ Logging চালু
logging.basicConfig(level=logging.INFO)

# ▶️ /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    full_name = user.full_name
    keyboard = [[InlineKeyboardButton("📞 নম্বর যাচাই করুন", callback_data="check_number")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_msg = f"""👋 হ্যালো {full_name}!
📱 এই বট দিয়ে আপনি যে কোন মোবাইল নম্বরের অপারেটর, দেশ, টাইপ এবং লোকেশন বের করতে পারবেন।

🔍 একটি নম্বর যাচাই করতে লিখুন:
`/phone 01712345678`

✅ উদাহরণ: `/phone 01812345678`
"""
    await update.message.reply_text(welcome_msg, reply_markup=reply_markup, parse_mode="Markdown")

# 📞 নম্বর চেক করার কমান্ড
async def phone_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ দয়া করে একটি মোবাইল নম্বর দিন।\nউদাহরণ: /phone 01712345678")
        return

    number = context.args[0]
    url = f"https://api.sumanjay.cf/phone/{number}"

    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(url)
            data = res.json()

        if "success" in data and data["success"] is False:
            await update.message.reply_text("❌ নম্বরটি সঠিক নয় বা তথ্য পাওয়া যায়নি।")
            return

        reply = f"🔎 মোবাইল নম্বর বিশ্লেষণ\n\n"
        reply += f"📱 নম্বর: {number}\n"
        reply += f"🌍 দেশ: {data.get('country', 'N/A')}\n"
        reply += f"🏢 অপারেটর: {data.get('operator', 'N/A')}\n"
        reply += f"📶 টাইপ: {data.get('type', 'N/A')}\n"
        reply += f"📍 লোকেশন: {data.get('location', 'অজানা')}"

        await update.message.reply_text(reply)

    except Exception as e:
        logging.error(e)
        await update.message.reply_text("⚠️ সার্ভার থেকে তথ্য আনা যায়নি। পরে আবার চেষ্টা করুন।")

# ▶️ Main Function
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("phone", phone_lookup))
    app.run_polling()

if __name__ == "__main__":
    main()
