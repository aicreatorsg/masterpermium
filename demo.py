import random
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, ContextTypes

TOKEN = '7401428392:AAFUuF9gVHhdoxVvDbyZcAGQc-hqqrCrG7I'

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Update this path to the folder containing your images



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
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data in ['BDG', 'Tiranga', '99 Club', 'TC Lottery', 'Lottery9']:
        platform_name = query.data
        follow_up_message = f"""
        🎉 Great Choice! 🎉

        You've selected **{platform_name}**!

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
        await query.edit_message_text(text=follow_up_message, parse_mode=ParseMode.MARKDOWN,
                                      reply_markup=game_reply_markup)

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

    elif query.data in ['mines', 'tower']:
        game_data = {
            'mines': (1, 28),
            'tower': (30, 42)
        }
        game_name = query.data
        image_range = game_data[game_name]

        impressive_message = "👇 **Your Result is Below** 👇"

        image_number = random.randint(*image_range)
        image_path = os.path.join( f'{image_number}.png')

        try:
            with open(image_path, 'rb') as img:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=img)

            await query.message.reply_text(impressive_message, parse_mode=ParseMode.MARKDOWN)

        except Exception as e:
            logger.error(f"Error sending photo: {e}")
            await query.message.reply_text("Sorry, an error occurred while sending the photo.")


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

    app.add_error_handler(error)

    app.run_polling()


if __name__ == '__main__':
    main()
