from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import asyncio  # To handle delays during scraping


# Define the GIF URL (you can use any online GIF URL)
LOADING_GIF_URL = "https://cdn.dribbble.com/users/197853/screenshots/5506993/media/f71129853a973c8426ef54cbf340fcb1.gif"


def twitter_email_scrapper(keyword, num_pages):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run browser in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Use ChromeDriverManager to automatically manage ChromeDriver
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)
    email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    all_emails = set()

    try:
        for page in range(num_pages):
            start = page * 10  # Google shows 10 results per page
            query = f"https://www.google.com/search?q={keyword}&start={start}"
            driver.get(query)
            time.sleep(3)  # Wait for the page to load

            # Get page source and extract emails
            page_source = driver.page_source
            emails = re.findall(email_regex, page_source)
            all_emails.update(emails)

            print(f"Page {page + 1} emails: {emails}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

    return list(all_emails)



def instagram_email_scrapper(keyword, num_pages):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run browser in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Use ChromeDriverManager to automatically manage ChromeDriver
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)
    email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    all_emails = set()

    try:
        for page in range(num_pages):
            start = page * 10  # Google shows 10 results per page
            query = f"https://www.google.com/search?q={keyword}&start={start}"
            driver.get(query)
            time.sleep(3)  # Wait for the page to load

            # Get page source and extract emails
            page_source = driver.page_source
            emails = re.findall(email_regex, page_source)
            all_emails.update(emails)

            print(f"Page {page + 1} emails: {emails}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

    return list(all_emails)




def tiktok_email_scrapper(keyword, num_pages):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run browser in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Use ChromeDriverManager to automatically manage ChromeDriver
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)
    email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    all_emails = set()

    try:
        for page in range(num_pages):
            start = page * 10  # Google shows 10 results per page
            query = f"https://www.google.com/search?q={keyword}&start={start}"
            driver.get(query)
            time.sleep(3)  # Wait for the page to load

            # Get page source and extract emails
            page_source = driver.page_source
            emails = re.findall(email_regex, page_source)
            all_emails.update(emails)

            print(f"Page {page + 1} emails: {emails}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

    return list(all_emails)



def validate_emails(email_list):
    
    email_regex = re.compile(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )

    valid_emails = set()  # Use a set to avoid duplicates
    invalid_emails = set()

    for email in email_list:
        # Check if email matches the standard regex
        if email_regex.match(email):
            local_part, domain = email.split("@")
            # Additional checks to exclude invalid formats or suspicious entries
            if (
                "%" in email  # Encoded characters
                or "+" in local_part  # Plus signs in local part
                or ".png" in email.lower()  # PNG files
                or "http" in email.lower()  # URLs
                or email.lower().startswith("instagram.com")  # Instagram URL fragments
                or len(local_part) < 3  # Exclude very short local parts (e.g., x22)
            ):
                invalid_emails.add(email)
            else:
                valid_emails.add(email)
        else:
            invalid_emails.add(email)

    return list(valid_emails), list(invalid_emails)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send me a keyword (e.g., 'fashion', 'football') to get started.")


async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a keyword (e.g., 'fashion', 'football') and I'll provide you platform options.")


async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    context.user_data['keyword'] = user_input  # Store the keyword in user data
    keyboard = [
        [
            InlineKeyboardButton("Instagram", callback_data="instagram"),
            InlineKeyboardButton("Twitter", callback_data="twitter"),
            InlineKeyboardButton("TikTok", callback_data="tiktok"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"You entered: {user_input}. Select a platform to scrape emails from:",
        reply_markup=reply_markup
    )


async def handle_platform_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query

    platform = query.data  # Extract the selected platform
    keyword = context.user_data.get('keyword', 'Unknown')  # Retrieve the stored keyword

    # Send the initial message
    await query.edit_message_text(
        text=f"You selected {platform.capitalize()} for the keyword: '{keyword}'. Scraping will start soon!"
    )

    # Send loading GIF
    gif_message = await query.message.reply_animation(animation=LOADING_GIF_URL, caption="Scraping in progress...")

    # Scraping Logic
    try:
        if platform == "instagram":
            final_keywords = f'site:instagram.com "{keyword}" "@gmail.com" "k+" "l+" "likes" "followers"'
            scrapped_emails = instagram_email_scrapper(final_keywords, num_pages=5)
        elif platform == "twitter":
            final_keywords = f'site:twitter.com "{keyword}" "@gmail.com" "k+"'
            scrapped_emails = twitter_email_scrapper(final_keywords, num_pages=5)
        elif platform == "tiktok":
            final_keywords = f'site:tiktok.com "{keyword}" "@gmail.com" "k+"'
            scrapped_emails = tiktok_email_scrapper(final_keywords, num_pages=5)
        else:
            scrapped_emails = []

        # Validate emails
        valid_emails, invalid_emails = validate_emails(scrapped_emails)
        print("\n\n")
        print(valid_emails)


        # Delete the GIF once scraping is complete
        await gif_message.delete()

        # Send the results

        if valid_emails:
            await query.message.reply_text(f"Scraping completed! Here are the valid emails:\n{',\n'.join(valid_emails)}")
        else:
            await query.message.reply_text("Scraping completed, but no valid emails were found.")

    except Exception as e:
        # Handle errors
        await gif_message.delete()
        await query.message.reply_text(f"An error occurred during scraping: {str(e)}")


# Main Function
def main():
    bot_token = "7678005643:AAG9C7MMhzMW9QJtg7b_5xPYH6GPHLz9a4w"
    app = ApplicationBuilder().token(bot_token).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", helper))

    # Message Handler for Keywords
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))

    # Callback Query Handler for Platform Selection
    app.add_handler(CallbackQueryHandler(handle_platform_selection))

    # Start Polling
    app.run_polling()


if __name__ == "__main__":
    main()
