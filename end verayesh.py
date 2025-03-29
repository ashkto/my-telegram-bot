import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "7586636738:AAGHfUceAOaElWg9DfjOaz04yo5fXdsihXk"
PUBLIC_CHANNEL = "-1002105319000"  # آیدی کانال عمومی
PRIVATE_CHANNEL = "-1002416426405"  # آیدی کانال خصوصی
BOT_USERNAME = "movieboxallbot"  # نام کاربری ربات

bot = telebot.TeleBot(TOKEN)

# **ذخیره دکمه‌های قبلی برای به‌روزرسانی بعدی**
button_storage = {}

### ✅ دستور /add (افزودن دکمه‌های زیر هم به پست)
@bot.message_handler(commands=['add'])
def add_download_buttons(message):
    try:
        parts = message.text.split()
        if len(parts) < 4 or len(parts) % 2 == 1:
            bot.reply_to(message, "❌ فرمت اشتباه! استفاده صحیح:\n"
                                  "`/add آیدی_پیام_عمومی آیدی_پیام_خصوصی1 عنوان1 ...`",
                                  parse_mode="Markdown")
            return

        public_msg_id = parts[1]
        private_msg_ids = parts[2::2]
        titles = parts[3::2]

        # بررسی اینکه آیا قبلاً دکمه‌ای وجود داشته یا نه
        existing_buttons = button_storage.get(public_msg_id, [])

        # افزودن دکمه‌های جدید
        for private_msg_id, title in zip(private_msg_ids, titles):
            existing_buttons.append(InlineKeyboardButton(f"📥 {title}", url=f"https://t.me/{BOT_USERNAME}?start={private_msg_id}"))

        # ذخیره دکمه‌ها برای استفاده‌های بعدی
        button_storage[public_msg_id] = existing_buttons

        # ایجاد دکمه‌ها به صورت زیر هم
        markup = InlineKeyboardMarkup()
        for button in existing_buttons:
            markup.add(button)

        bot.edit_message_reply_markup(PUBLIC_CHANNEL, int(public_msg_id), reply_markup=markup)
        bot.reply_to(message, "✅ دکمه‌های دانلود **به‌روزرسانی شدند و به‌صورت زیر هم اضافه شدند!**")

    except Exception as e:
        bot.reply_to(message, f"❌ خطا: {e}")

### ✅ دستور /add_inline (افزودن دکمه‌های کنار هم به پست)
@bot.message_handler(commands=['add_inline'])
def add_inline_buttons(message):
    try:
        parts = message.text.split()
        if len(parts) < 4 or len(parts) % 2 == 1:
            bot.reply_to(message, "❌ فرمت اشتباه! استفاده صحیح:\n"
                                  "`/add_inline آیدی_پیام_عمومی آیدی_پیام_خصوصی1 عنوان1 ...`",
                         parse_mode="Markdown")
            return

        public_msg_id = parts[1]
        private_msg_ids = parts[2::2]
        titles = parts[3::2]

        # بررسی اینکه آیا قبلاً دکمه‌ای وجود داشته یا نه
        existing_buttons = button_storage.get(public_msg_id, [])

        # افزودن دکمه‌های جدید
        for private_msg_id, title in zip(private_msg_ids, titles):
            existing_buttons.append(InlineKeyboardButton(f"📥 {title}", url=f"https://t.me/{BOT_USERNAME}?start={private_msg_id}"))

        # ذخیره دکمه‌ها برای استفاده‌های بعدی
        button_storage[public_msg_id] = existing_buttons

        # نمایش دکمه‌ها به صورت ۲ یا ۳ تایی در هر ردیف
        markup = InlineKeyboardMarkup()
        for i in range(0, len(existing_buttons), 3):  # گروه‌بندی سه‌تایی
            markup.row(*existing_buttons[i:i+3])  # اگر کمتر از ۳ دکمه باشد، همان تعداد نمایش داده می‌شود

        bot.edit_message_reply_markup(PUBLIC_CHANNEL, int(public_msg_id), reply_markup=markup)
        bot.reply_to(message, "✅ دکمه‌های دانلود **به‌روزرسانی شدند و به‌صورت ۲ یا ۳ تایی اضافه شدند!**")

    except Exception as e:
        bot.reply_to(message, f"❌ خطا: {e}")

### ✅ دستور /remove_buttons (حذف دکمه‌های یک پست)
@bot.message_handler(commands=['remove_buttons'])
def remove_buttons(message):
    try:
        parts = message.text.split()
        if len(parts) != 2:
            bot.reply_to(message, "❌ فرمت اشتباه! استفاده صحیح:\n"
                                  "`/remove_buttons آیدی_پیام_عمومی`", parse_mode="Markdown")
            return

        public_msg_id = parts[1]

        # حذف دکمه‌ها از حافظه
        button_storage.pop(public_msg_id, None)

        # حذف دکمه‌ها از پیام
        bot.edit_message_reply_markup(PUBLIC_CHANNEL, int(public_msg_id), reply_markup=InlineKeyboardMarkup())
        bot.reply_to(message, "✅ دکمه‌های دانلود از این پست حذف شدند!")

    except Exception as e:
        bot.reply_to(message, f"❌ خطا در حذف دکمه‌ها: {e}")

### ✅ دریافت چندین ویدیو هنگام کلیک روی دکمه دانلود
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    args = message.text.split()

    if len(args) > 1:
        private_msg_ids = args[1].split('-')  # چندین آیدی را جدا کنیم

        for private_msg_id in private_msg_ids:
            if private_msg_id.isdigit():
                private_msg_id = int(private_msg_id)
                try:
                    bot.forward_message(chat_id=user_id, from_chat_id=PRIVATE_CHANNEL, message_id=private_msg_id)
                except Exception:
                    bot.send_message(user_id, f"❌ ویدیویی با آیدی {private_msg_id} یافت نشد.")
            else:
                bot.send_message(user_id, "❌ آیدی پیام نامعتبر است.")
    else:
        bot.send_message(user_id, "👋 خوش آمدید! لطفاً برای دریافت ویدیو روی دکمه دانلود کلیک کنید.")

bot.polling()
