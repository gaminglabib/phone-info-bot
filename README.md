
# Phone Number Info Telegram Bot for Render

এই বটটি Render-এ Deploy করার জন্য তৈরি। এটা Telegram Bot API এবং numlookupapi.com এর মাধ্যমে ফোন নাম্বারের ইনফরমেশন নিয়ে আসে।

## Features
- /start কমান্ডে স্বাগত বার্তা
- /find <number> কমান্ডে নাম্বারের দেশ, অপারেটর, টাইপ ইত্যাদি দেখায়
- Auto-ping সিস্টেম যা বটকে Render এ সবসময় online রাখে
- ইউজার লোগ CSV ফাইলে সংরক্ষণ করে

## Setup Instructions

1. **Clone or Download** this repo
2. Replace `YOUR_BOT_TOKEN` in `bot.py` with your Telegram bot token
3. Replace `https://your-render-app-name.onrender.com` in `bot.py` with your Render app URL
4. Optionally, get your own API key from [numlookupapi.com](https://numlookupapi.com) and replace the `NUMLOOKUP_API_KEY` variable
5. Create a new Web Service on Render:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
6. Deploy and enjoy!

## Notes
- Free API plan allows limited requests per day
- Make sure to keep your bot token and API key secure

## Contact
Developed by Toxic Digonto.
