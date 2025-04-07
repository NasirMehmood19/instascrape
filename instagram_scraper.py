
import time
import pickle
import psycopg2
import requests
import cloudinary
import cloudinary.uploader
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import os
import base64

DATABASE_URL = os.getenv("DATABASE_URL")

# --- Cloudinary Configuration ---
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)



# --- Selenium WebDriver Setup ---
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=375,812")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(
    "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Mobile Safari/537.36"
)

# --- Instagram Pages ---
INSTAGRAM_PAGES = {
    "Kim Kardashian": "https://www.instagram.com/kimkardashian/",
    # "Kylie Jenner": "https://www.instagram.com/kyliejenner/",
    # "Rihanna": "https://www.instagram.com/badgalriri/",
    # "Kanye West": "https://www.instagram.com/ye/",
    # "Justin Bieber": "https://www.instagram.com/justinbieber/",
    # "Hailey Bieber": "https://www.instagram.com/haileybieber/",
    # "Selena Gomez": "https://www.instagram.com/selenagomez/",
    # "Henry Cavill": "https://www.instagram.com/HenryCavill/",
    # "Emma Roberts": "https://www.instagram.com/emmaroberts/",
    # "Reese Witherspoon": "https://www.instagram.com/reesewitherspoon/",
    # "Shakira": "https://www.instagram.com/shakira/",
    # "Beyoncé": "https://www.instagram.com/beyonce/",
    # "Lady Gaga": "https://www.instagram.com/ladygaga/",
    # "Ariana Grande": "https://www.instagram.com/arianagrande/",
    # "Billie Eilish": "https://www.instagram.com/billieeilish/",
    # "Miley Cyrus": "https://www.instagram.com/mileycyrus/",
    # "Gigi Hadid": "https://www.instagram.com/gigihadid/",
    # "Zayn Malik": "https://www.instagram.com/zayn/",
    # "Tom Cruise": "https://www.instagram.com/tomcruise/",
    # "Barry Keoghan": "https://www.instagram.com/barrykeoghansource/",
    # "Meghan Markle": "https://www.instagram.com/meghan/",
    # "Kendall Jenner": "https://www.instagram.com/kendalljenner/",
    # "Kris Jenner": "https://www.instagram.com/krisjenner/",
    # "Khloé Kardashian": "https://www.instagram.com/khloekardashian/",
    # "Kourtney Kardashian": "https://www.instagram.com/kourtneykardash/",
    # "Jeremy Renner": "https://www.instagram.com/jeremyrenner/?hl=en",
    # "Chris Hemsworth": "https://www.instagram.com/chrishemsworth/",
    # "Ed Sheeran": "https://www.instagram.com/teddysphotos/",
    # "Sydney Sweeney": "https://www.instagram.com/sydney_sweeney/",
    # "Anne Hathaway": "https://www.instagram.com/annehathaway/",
    # "Jennifer Lopez": "https://www.instagram.com/jlo/",
    # "Jennifer Garner": "https://www.instagram.com/jennifer.garner/",
    # "Jennifer Aniston": "https://www.instagram.com/jenniferaniston/",
    # "Jennifer Lawrence": "https://www.instagram.com/1jnnf/",
    # "The Royal Family": "https://www.instagram.com/theroyalfamily/",
    # "Cardi B": "https://www.instagram.com/iamcardib/",
    # "Soompi": "https://www.instagram.com/soompi/",
    # "Katy Perry": "https://www.instagram.com/katyperry/",
    # "Paris Hilton": "https://www.instagram.com/parishilton/",
    # "Zendaya": "https://www.instagram.com/zendaya/",
    # "Jenna Ortega": "https://www.instagram.com/jennaortega/",
    # "Netflix": "https://www.instagram.com/netflix/",
    # "Tom Hanks": "https://www.instagram.com/tomhanks/",
    # "Vin Diesel": "https://www.instagram.com/vindiesel/",
    # "Robert Downey Jr.": "https://www.instagram.com/robertdowneyjr/",
    # "Prince and Princess of Wales": "https://www.instagram.com/princeandprincessofwales",
    # "The Royal Family": "https://www.instagram.com/theroyalfamily",
    # "Sarah Ferguson": "https://www.instagram.com/sarahferguson15",
    # "Meghan": "https://www.instagram.com/meghan",
    # "Duke and Duchess of Sussex Daily": "https://www.instagram.com/dukeandduchessofsussexdaily",
    # "Rebecca English": "https://www.instagram.com/byrebeccaenglish",
    # "Taylor Swift": "https://www.instagram.com/taylorswift",
    # "Killatrav": "https://www.instagram.com/killatrav",
    # "Princess Eugenie": "https://www.instagram.com/princesseugenie",
    # "Ryan Reynolds": "https://www.instagram.com/vancityreynolds",
    # "Gigi Hadid": "https://www.instagram.com/gigihadid"
}

# --- Load Instagram Cookies ---
def load_cookies(driver):
    try:
        # Fetch the base64 encoded cookie data from the environment variable
        base64_cookie_data = os.getenv("COOKIES_BASE64")  # Replace with your secret variable name

        if not base64_cookie_data:
            print("⚠️ Base64 cookie data is missing from the environment variable.")
            return

        # Decode the base64 string into the original cookie file
        cookie_data = base64.b64decode(base64_cookie_data)

        # Load the cookies from the decoded data
        cookies = pickle.loads(cookie_data)

        # Add cookies to the Selenium WebDriver
        for cookie in cookies:
            if "sameSite" in cookie and cookie["sameSite"] not in ["Strict", "Lax", "None"]:
                del cookie["sameSite"]
            driver.add_cookie(cookie)

        print("✅ Cookies loaded successfully!")
    
    except Exception as e:
        print(f"⚠️ Error loading cookies from base64: {e}")



# --- Extract Latest Post & Post Image ---
def get_instagram_post(page_url):
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.instagram.com/")
    time.sleep(5)

    load_cookies(driver)
    driver.refresh()
    time.sleep(5)

    driver.get(page_url)
    time.sleep(10)

    post = None

    # --- Extract Latest Post URL ---
    try:
        post_links = driver.find_elements(By.TAG_NAME, "a")
        for link in post_links:
            url = link.get_attribute("href")
            if url and ("/p/" in url or "/reel/" in url):
                post = {"url": url, "image_url": None, "timestamp": None}
                break  # Only take the first/latest post
    except Exception as e:
        print(f"⚠️ Error finding post URL: {e}")

    if post:
        driver.get(post["url"])
        time.sleep(5)

        # --- Extract Post Image ---
        try:
            image_element = driver.find_element(By.XPATH, "//div[contains(@class, '_aagv')]/img")
            post["image_url"] = image_element.get_attribute("src")
            print(f"✅ Post Image URL: {post['image_url']}")
        except Exception as e:
            print(f"⚠️ Could not fetch post image: {e}")

        # --- Extract Timestamp ---
        try:
            time_element = driver.find_element(By.TAG_NAME, "time")
            ts_str = time_element.get_attribute("datetime")
            if ts_str:
                utc_time = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                post["timestamp"] = utc_time.astimezone(timezone(timedelta(hours=5)))  # Convert to Pakistan Time (UTC+5)
        except Exception as e:
            print(f"⚠️ Could not get timestamp for {post['url']}: {e}")

    driver.quit()
    return post

# --- Upload Post Image to Cloudinary ---
def upload_to_cloudinary(image_url, page_name):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        cloud_response = cloudinary.uploader.upload(response.raw, folder="instagram_posts", public_id=page_name)
        return cloud_response["secure_url"]
    return None

# --- Scrape & Store Data in PostgreSQL ---
def scrape_instagram():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Create table if not exists
    create_table_query = """
    CREATE TABLE IF NOT EXISTS instagram_posts (
        id SERIAL PRIMARY KEY,
        page_name TEXT NOT NULL,
        link TEXT NOT NULL UNIQUE,
        post_image TEXT,
        timestamp TIMESTAMP
    );
    """
    cursor.execute(create_table_query)
    conn.commit()

    for page_name, page_url in INSTAGRAM_PAGES.items():
        print(f"🔍 Scraping Instagram page: {page_name}")
        post = get_instagram_post(page_url)

        if post and post["image_url"]:
            print(f"✅ Latest Post: {post['url']} | Image: {post['image_url']} | timestamp: {post['timestamp']}")

            # Upload post image to Cloudinary
            cloudinary_url = upload_to_cloudinary(post["image_url"], page_name)

            # Insert into DB only if new post is found
            cursor.execute("SELECT link FROM instagram_posts WHERE page_name = %s ORDER BY timestamp DESC LIMIT 1", (page_name,))
            result = cursor.fetchone()

            if result and result[0] != post["url"]:
                print(f"🔄 Updating {page_name} with new post...")
                cursor.execute(
                    "INSERT INTO instagram_posts (page_name, link, post_image, timestamp) VALUES (%s, %s, %s, %s)",
                    (page_name, post["url"], cloudinary_url, post["timestamp"])
                )
            elif not result:
                print(f"🆕 Adding first post for {page_name}...")
                cursor.execute(
                    "INSERT INTO instagram_posts (page_name, link, post_image, timestamp) VALUES (%s, %s, %s, %s)",
                    (page_name, post["url"], cloudinary_url, post["timestamp"])
                )

            conn.commit()
        else:
            print(f"❌ No new post found for {page_name}")

    cursor.close()
    conn.close()
    print("✅ Instagram scraping complete!")

# --- Main Loop ---
scrape_instagram()
