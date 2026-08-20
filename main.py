import os
import telebot
from telebot import types
import google.generativeai as genai

# Your Credentials
BOT_TOKEN = "8877574460:AAE6XuucOACO_rzpLE_bxyVbWBp2jx34VZk"
GEMINI_API_KEY = "AIza..." # এখানে আপনার নতুন জেমিনি কি দিন (অবশ্যই AIza দিয়ে শুরু হওয়া কি)

genai.configure(api_key=GEMINI_API_KEY)
bot = telebot.TeleBot(BOT_TOKEN)
model = genai.GenerativeModel('gemini-1.5-flash')

def math_bold(text):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    bold = "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"
    trans = str.maketrans(normal, bold)
    return text.translate(trans)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn_text = math_bold("Create Website")
    button = types.InlineKeyboardButton(f"{btn_text} 🌐", callback_data="make_web")
    markup.add(button)
    welcome_msg = math_bold("WELCOME! I CAN CREATE A PROFESSIONAL WEBSITE FOR YOU. CLICK THE BUTTON BELOW TO START.")
    bot.send_message(message.chat.id, welcome_msg, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "make_web")
def ask_prompt(call):
    prompt_msg = math_bold("PLEASE DESCRIBE YOUR WEBSITE IN DETAIL.")
    msg = bot.send_message(call.message.chat.id, prompt_msg)
    bot.register_next_step_handler(msg, generate_website)

def generate_website(message):
    user_prompt = message.text
    chat_id = message.chat.id
    bot.reply_to(message, math_bold("GENERATING YOUR WEBSITE CODE... PLEASE WAIT."))
    try:
        full_prompt = f"Create a professional single-file HTML website with CSS and JS for: {user_prompt}. Provide ONLY source code. No explanations, no backticks."
        response = model.generate_content(full_prompt)
        code = response.text.strip().replace("```html", "").replace("```", "")
        filename = f"index_{chat_id}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)
        with open(filename, "rb") as f:
            bot.send_document(chat_id, f, caption=f"✅ {math_bold('YOUR WEBSITE FILE IS READY!')}", visible_file_name="index.html")
        os.remove(filename)
    except Exception as e:
        bot.send_message(chat_id, math_bold("ERROR! TRY AGAIN LATER."))

if __name__ == "__main__":
    bot.infinity_polling()
