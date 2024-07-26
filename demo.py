import random
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = '7401428392:AAFUuF9gVHhdoxVvDbyZcAGQc-hqqrCrG7I'

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Dictionary to store user states
user_states = {}

# Fake database of usernames
valid_usernames = ["user1", "user2", "user3"]

# Function to send a random image for Mines or Tower
async def send_random_image(query, context, game_name, image_range):
    image_number = random.randint(*image_range)
    image_path = os.path.join(f'{image_number}.png')

    try:
        with open(image_path, 'rb') as img:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=img)
            await query.message.reply_text("👇 **Your Result is Below** 👇", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.error(f"Error sending photo: {e}")
        await query.message.reply_text("Sorry, an error occurred while sending the photo.")

async def start(update: Update, context: CallbackContext) -> None:
    welcome_message = """
    🎉 **Welcome to GameMasterPremium Bot!** 🎉

    Hey, GameMaster! 🌟 Ready to turn the odds in your favor? 🚀 Our bot predicts winning signals for top games like **Aviator, Mines, Limbo**, and **Tower**. Play on **BDG, Tiranga, 99 Club, TC Lottery**, or **Lottery9** and watch your luck soar! 🍀

    🎯 **Why GameMaster Bot?** 🎯

    🔮 **Accurate Signals**  
    ⚡ **Real-time Alerts**  
    🌐 **Multi-Platform Support**

    💎 **Premium Bot:** Unlimited signals!

    💥 **Get Started:** 💥

    1. **Join Us:** Connect with winners! 🏅  
    2. **Activate Signals:** Easy steps! 🔧  
    3. **Win Big:** Maximize your gains! 💰

    📞 **24/7 Support:** We're here for you!

    ---

    Hit **/start** to begin your winning journey! 🏆

    💌 **Special Offer:** 20% off Premium! Code: **WINBIG20**

    👇 **Please choose your platform to continue:**
    """

    keyboard = [
        [InlineKeyboardButton("BDG", callback_data='BDG')],
        [InlineKeyboardButton("Tiranga", callback_data='Tiranga')],
        [InlineKeyboardButton("99 Club", callback_data='99 Club')],
        [InlineKeyboardButton("TC Lottery", callback_data='TC Lottery')],
        [InlineKeyboardButton("Lottery9", callback_data='Lottery9')],
        [InlineKeyboardButton("YOLO27", callback_data='YOLO')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data in ['BDG', 'Tiranga', '99 Club', 'TC Lottery', 'Lottery9', 'YOLO']:
        await query.edit_message_text(text=f"You've selected **{query.data}**. Please enter your username:")
        user_states[query.from_user.id] = {'platform': query.data, 'awaiting_username': True}
    elif query.data.startswith('mines_'):
        mines_choice = query.data.split('_')[1]
        await send_random_image(query, context, 'mines', (1, 28))
    elif query.data == 'mines':
        mines_keyboard = [
            [InlineKeyboardButton("1💣", callback_data='mines_1')],
            [InlineKeyboardButton("2💣💣", callback_data='mines_2')],
            [InlineKeyboardButton("3💣💣💣", callback_data='mines_3')],
            [InlineKeyboardButton("4💣💣💣💣", callback_data='mines_4')],
        ]
        mines_reply_markup = InlineKeyboardMarkup(mines_keyboard)
        await query.edit_message_text(text="Choose the number of mines:", reply_markup=mines_reply_markup)
    elif query.data == 'tower':
        await send_random_image(query, context, 'tower', (30, 42))
    elif query.data in ['aviator', 'limbo']:
        result = round(random.uniform(1.0, 4.0), 2)
        percentage = random.randint(80, 100)
        result_message = f"""
        🎰 {query.data.capitalize()} Result: 

        <b>{result}</b>

        🎉 Congratulations, your result is accurate! 🎉
        {percentage}%
        """

        await query.edit_message_text(text=result_message, parse_mode=ParseMode.HTML)


async def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in user_states and user_states[user_id].get('awaiting_username'):
        username = update.message.text
        if username in valid_usernames:
            platform = user_states[user_id]['platform']
            follow_up_message = f"""
            🎉 Great Choice! 🎉

            You've selected **{platform}**!

            You're almost ready to start winning big! 🌟 Our bot boasts an impressive accuracy rate of 97% for our Premium Bot. Get ready to experience the thrill of precise predictions!

            🎮 Please choose your game: 🎮

            ✈️ Aviator
            💣 Mines
            🎲 Limbo
            🏰 Tower

            Tap on your game of choice and let’s get those winning signals rolling! 🚀💰
            """

            game_keyboard = [
                [InlineKeyboardButton("✈️ Aviator💵", callback_data='aviator')],
                [InlineKeyboardButton("💣 Mines💵", callback_data='mines')],
                [InlineKeyboardButton("🎲 Limbo💵", callback_data='limbo')],
                [InlineKeyboardButton("🏰 Tower💵", callback_data='tower')],
            ]

            game_reply_markup = InlineKeyboardMarkup(game_keyboard)
            await update.message.reply_text(follow_up_message, parse_mode=ParseMode.MARKDOWN, reply_markup=game_reply_markup)
            user_states.pop(user_id)
        else:
            invalid_username_message = """
            🚫 Invalid Username! 🚫

            We're sorry, but the username you entered is invalid. 😞

            To activate this feature, you'll need to purchase the bot. 🎉

            Good news! We're offering a 70% discount just for you! 🎊

            💸 Grab the deal now and enjoy the full benefits! 💸

            Don't miss out! 🔥
            """
            keyboard = [
                [InlineKeyboardButton("Buy the Bot", url='https://t.me/your_other_bot')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(invalid_username_message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def help_command(update: Update, context: CallbackContext) -> None:
    help_message = """
    **GameMasterPremium Bot Help**

    Here are the commands you can use:

    /start - Start interacting with the bot
    /help - Show this help message

    For any issues or questions, please contact our support team.
    """
    await update.message.reply_text(help_message, parse_mode=ParseMode.MARKDOWN)


def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main() -> None:
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_error_handler(error)

    app.run_polling()


if __name__ == '__main__':
    main()
