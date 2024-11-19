from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

def twitter_email_scrapper(keyword, num_pages=5):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run browser in headless mode
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")

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
    # Define a stricter regular expression for valid email format
    email_regex = re.compile(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )
    
    valid_emails = []
    invalid_emails = []

    for email in email_list:
        # Check if email matches the valid format
        if email_regex.match(email):
            # Additional checks to exclude emails containing encoded characters or invalid domains
            if "%22" in email or "%2522" in email or "+" in email.split("@")[0]:
                invalid_emails.append(email)
            else:
                valid_emails.append(email)
        else:
            invalid_emails.append(email)

    return valid_emails, invalid_emails

# Test the Selenium script
if __name__ == "__main__":
    keyword = 'site:twitter.com "fashion" "@gmail.com" "k+" '
    emails = twitter_email_scrapper(keyword, num_pages=4)
    print("Extracted Emails:", emails)
    print("/n/n")
    print("Applying the validator")

    valid_emails, invalid_emails = validate_emails(emails)

    # Output results

    print("/n/n")
    print("Valid Emails:")
    for email in valid_emails:
        print(email)

    print("\nInvalid Emails:")
    for email in invalid_emails:
        print(email)
