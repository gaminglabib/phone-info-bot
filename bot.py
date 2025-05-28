
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.markdown import hbold
from aiogram import F
import aiohttp
import asyncio
import csv
from datetime import datetime
from fastapi import FastAPI
import uvicorn
import os

API_TOKEN = 'YOUR_BOT_TOKEN'
NUMLOOKUP_API_KEY = 'demo'  # তোমার ইচ্ছা হলে numlookupapi.com থেকে API KEY নিতে পারো

# Logging setup
logging.basicConfig(level=logging.INFO)

# Telegram bot init
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# FastAPI server (Render এর জন্য)
app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Bot is alive!"}

# CSV Logging Function
def log_query(user_id, full_name, number):
    with open("queries.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), user_id, full_name, number])

# /start command
@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    full_name = message.from_user.full_name
    await message.answer(
        f"👋 প্রিয় {full_name},\n\n"
        "📞 ফোন নাম্বার তথ্য জানতে /find <নাম্বার> লিখুন\n\n"
        "উদাহরণ: `/find 01812345678`",
        parse_mode=ParseMode.MARKDOWN
    )

# /find command
@dp.message(F.text.startswith("/find"))
async def find_number(message: Message):
    try:
        parts = message.text.split()
        if len(parts) != 2:
            return await message.reply("⚠️ দয়া করে ঠিকভাবে লিখুন:\n/find 01812345678")

        number = parts[1]

        # API request
        url = f"https://api.numlookupapi.com/v1/validate/{number}?apikey={NUMLOOKUP_API_KEY}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()

        if "valid" in data and data["valid"]:
            result = (
                f"📞 **ফোন নাম্বার বিশ্লেষণ:**\n"
                f"• নাম্বার: `{data.get('international_format')}`\n"
                f"• দেশ: {data.get('country_name')}\n"
                f"• অপারেটর: {data.get('carrier')}\n"
                f"• টাইপ: {data.get('line_type')}\n"
            )
            if data.get("is_spam"):
                result += "\n⚠️ **স্প্যাম হিসেবে চিহ্নিত!**"

            await message.reply(result, parse_mode=ParseMode.MARKDOWN)

            # Log this
            log_query(message.from_user.id, message.from_user.full_name, number)

        else:
            await message.reply("❌ সঠিক ফোন নাম্বার পাওয়া যায়নি বা ইনভ্যালিড।")
    except Exception as e:
        await message.reply("⚠️ কিছু সমস্যা হয়েছে, পরে আবার চেষ্টা করুন।")

# Auto-ping loop to prevent sleep
async def auto_ping():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                await session.get("https://your-render-app-name.onrender.com")
        except:
            pass
        await asyncio.sleep(600)  # প্রতি ১০ মিনিটে ping

# Bot runner
async def main():
    asyncio.create_task(auto_ping())  # start ping loop
    await dp.start_polling(bot)

# Uvicorn runner for FastAPI (Render needs this)
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
