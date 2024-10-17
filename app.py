import requests
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# URL of the webpage
url = 'https://www.propertyfinder.ae/en/search?l=9831&c=2&bdr%5B%5D=2&fu=0&rp=y&ob=nd'

# Set headers to mimic a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Time interval constant in seconds (set to 20 seconds)
TIME_INTERVAL = 1200  # Change this value to adjust the time interval

previous_number = None  # To store the previous number of properties
bot_token = '7890942178:AAGbG0knGeJH7VFYvdzHwvUgwQ18wWO9TJM'  # Replace with your bot token

def fetch_properties_count():
    """Fetch the number of properties from the webpage."""
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        page_content = response.text

        # Search for the substring that matches the "<number> properties" pattern
        match = re.search(r'(\d+) properties', page_content)

        if match:
            # Extract the number of properties
            return int(match.group(1))
        else:
            return None
    else:
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(f'Monitoring has started. You will receive updates every {TIME_INTERVAL} seconds.')

    # Send the current property count immediately
    await send_property_count(context, chat_id=update.message.chat_id)

    # Start sending updates every TIME_INTERVAL seconds using the JobQueue
    context.job_queue.run_repeating(send_property_count_job, interval=TIME_INTERVAL, first=TIME_INTERVAL, chat_id=update.message.chat_id)

async def send_property_count(context: ContextTypes.DEFAULT_TYPE, chat_id: int) -> None:
    """Fetch the property count and send a message if it changes."""
    global previous_number
    current_number = fetch_properties_count()

    if current_number is not None:
        message = f"Current number of properties: {current_number}"

        # Compare with the previous number
        if previous_number is not None:
            if current_number > previous_number:
                message += f"\nALERT: The number of properties has INCREASED from {previous_number} to {current_number}."
            elif current_number < previous_number:
                message += f"\nALERT: The number of properties has DECREASED from {previous_number} to {current_number}."

        # Update the previous number
        previous_number = current_number
        
        # Send message to the user
        await context.bot.send_message(chat_id=chat_id, text=message)

async def send_property_count_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fetch the property count and send a message if it changes, called by the job queue."""
    await send_property_count(context, chat_id=context.job.chat_id)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(bot_token).build()

    # Register the /start command handler
    application.add_handler(CommandHandler("start", start))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
