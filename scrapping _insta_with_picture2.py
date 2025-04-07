# import time
# import pickle
# import psycopg2
# import requests
# import cloudinary
# import cloudinary.uploader
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from datetime import datetime, timezone, timedelta
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # --- PostgreSQL Database ---
# DATABASE_URL = "postgresql://instaxrss_user:QGBb5ALqiBraZtjt1c1zoifa4Kf4G1Tu@dpg-cv7sqcqj1k6c739htp00-a.oregon-postgres.render.com/instaxrss"

# # --- Cloudinary Configuration ---
# cloudinary.config(
#     cloud_name="dka67k5av",
#     api_key="696938932641642",
#     api_secret="Ow7AilWBHGJnkotnC_YVR6xVa6M"  # Consider using environment variables for security
# )

# # --- Selenium WebDriver Setup ---
# insta_options = Options()
# insta_options.add_argument("--headless=new")
# insta_options.add_argument("--disable-gpu")
# insta_options.add_argument("--window-size=375,812")
# insta_options.add_argument("--disable-blink-features=AutomationControlled")
# insta_options.add_argument(
#     "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) "
#     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Mobile Safari/537.36"
# )

# INSTAGRAM_PAGES = {
#     "Kim Kardashian": "https://www.instagram.com/kimkardashian/"
#     # "Kylie Jenner": "https://www.instagram.com/kyliejenner/",
# }

# # --- Load Instagram Cookies ---
# def load_cookies(driver, file_path):
#     try:
#         cookies = pickle.load(open(file_path, "rb"))
#         for cookie in cookies:
#             driver.add_cookie(cookie)
#         print(f"✅ Cookies loaded from {file_path}!")
#     except Exception as e:
#         print(f"⚠️ Error loading cookies from {file_path}: {e}")

# # --- Extract Latest Post & Post Image ---
# def get_instagram_post(page_url):
#     driver = webdriver.Chrome(options=insta_options)
#     driver.get("https://www.instagram.com/")
#     time.sleep(5)

#     load_cookies(driver, "instagram_cookies.pkl")
#     driver.refresh()
#     time.sleep(5)

#     driver.get(page_url)
#     time.sleep(10)

#     # --- Extract Latest Post ---
#     posts = []
#     links = driver.find_elements(By.TAG_NAME, "a")
#     for link in links:
#         url = link.get_attribute("href")
#         if url and ("/p/" in url or "/reel/" in url):
#             posts.append({"url": url, "image_url": None, "timestamp": None})
#             if len(posts) == 1:  # Only need the latest post
#                 break

#     if posts:
#         post = posts[0]
#         driver.get(post["url"])
#         time.sleep(5)

#         # Extract post image
       
#         try:
#             image_element = driver.find_element(By.XPATH, "//div[contains(@class, '_aagv')]/img")
#             image_url = image_element.get_attribute("src")
#             print("Post Image URL:", image_url)

#         except Exception as e:
#             print(f"⚠️ Error: {e}")

#         # Extract timestamp
#         try:
#             time_element = driver.find_element(By.TAG_NAME, "time")
#             ts_str = time_element.get_attribute("datetime")
#             if ts_str:
#                 utc_time = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
#                 local_time = utc_time.astimezone(timezone(timedelta(hours=5)))  # Convert to Pakistan Time (UTC+5)
#                 post["timestamp"] = local_time
#         except Exception as e:
#             print(f"⚠️ Could not get timestamp for {post['url']}: {e}")

#     driver.quit()
#     return post if posts else None

# # --- Upload Post Image to Cloudinary ---
# def upload_to_cloudinary(image_url, page_name):
#     response = requests.get(image_url, stream=True)
#     if response.status_code == 200:
#         cloud_response = cloudinary.uploader.upload(response.raw, folder="instagram_posts", public_id=page_name)
#         return cloud_response["secure_url"]
#     return None

# # --- Scrape & Store Data in PostgreSQL ---
# def scrape_instagram():
#     conn = psycopg2.connect(DATABASE_URL)
#     cursor = conn.cursor()
    
#     # Create table if not exists
#     create_table_query = """
#     CREATE TABLE IF NOT EXISTS instagram_posts (
#         id SERIAL PRIMARY KEY,
#         page_name TEXT NOT NULL,
#         link TEXT NOT NULL,
#         post_image TEXT,
#         timestamp TIMESTAMP,
#         UNIQUE (page_name)
#     );
#     """
#     cursor.execute(create_table_query)
#     conn.commit()

#     for page_name, page_url in INSTAGRAM_PAGES.items():
#         print(f"Scraping Instagram page: {page_name}")
#         post = get_instagram_post(page_url)

#         if post and post["image_url"]:
#             print(f"Latest Post: {post['url']} | Image: {post['image_url']}")

#             # Upload post image to Cloudinary
#             cloudinary_url = upload_to_cloudinary(post["image_url"], page_name)

#             cursor.execute("SELECT link FROM instagram_posts WHERE page_name = %s", (page_name,))
#             result = cursor.fetchone()

#             if result:
#                 old_link = result[0]
#                 if old_link != post["url"]:
#                     print(f"Updating data for {page_name}")
#                     cursor.execute(
#                         "UPDATE instagram_posts SET link = %s, post_image = %s, timestamp = %s WHERE page_name = %s",
#                         (post["url"], cloudinary_url, post["timestamp"], page_name)
#                     )
#             else:
#                 cursor.execute(
#                     "INSERT INTO instagram_posts (page_name, link, post_image, timestamp) VALUES (%s, %s, %s, %s)",
#                     (page_name, post["url"], cloudinary_url, post["timestamp"])
#                 )
#             conn.commit()
#         else:
#             print(f"❌ No new post found for {page_name}")

#     cursor.close()
#     conn.close()
#     print("✅ Instagram scraping complete!")

# # --- Main Loop ---
# while True:
#     scrape_instagram()
#     print("Waiting 30 minutes before next scrape...")
#     time.sleep(60 * 30)






























# import time
# import pickle
# import psycopg2
# import requests
# import cloudinary
# import cloudinary.uploader
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from datetime import datetime, timezone, timedelta
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # --- PostgreSQL Database ---
# DATABASE_URL = "postgresql://instaxrss_user:QGBb5ALqiBraZtjt1c1zoifa4Kf4G1Tu@dpg-cv7sqcqj1k6c739htp00-a.oregon-postgres.render.com/instaxrss"

# # --- Cloudinary Configuration ---
# cloudinary.config(
#     cloud_name="dka67k5av",
#     api_key="696938932641642",
#     api_secret="Ow7AilWBHGJnkotnC_YVR6xVa6M"  # Consider using environment variables for security
# )

# # --- Selenium WebDriver Setup ---
# insta_options = Options()
# insta_options.add_argument("--headless=new")
# insta_options.add_argument("--disable-gpu")
# insta_options.add_argument("--window-size=375,812")
# insta_options.add_argument("--disable-blink-features=AutomationControlled")
# insta_options.add_argument(
#     "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) "
#     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Mobile Safari/537.36"
# )

# INSTAGRAM_PAGES = {
#     "Kim Kardashian": "https://www.instagram.com/kimkardashian/",
#     # "Kylie Jenner": "https://www.instagram.com/kyliejenner/",
#     "Kris Jenner": "https://www.instagram.com/krisjenner/"
# }

# # --- Load Instagram Cookies ---
# def load_cookies(driver, file_path):
#     try:
#         cookies = pickle.load(open(file_path, "rb"))
#         for cookie in cookies:
#             driver.add_cookie(cookie)
#         print(f"✅ Cookies loaded from {file_path}!")
#     except Exception as e:
#         print(f"⚠️ Error loading cookies from {file_path}: {e}")

# # --- Extract Latest Post & Post Image ---
# def get_instagram_post(page_url):
#     driver = webdriver.Chrome(options=insta_options)
#     driver.get("https://www.instagram.com/")
#     time.sleep(5)

#     load_cookies(driver, "instagram_cookies.pkl")
#     driver.refresh()
#     time.sleep(5)

#     driver.get(page_url)
#     time.sleep(10)

#     post = None

#     # --- Extract Latest Post URL ---
#     try:
#         post_links = driver.find_elements(By.TAG_NAME, "a")
#         for link in post_links:
#             url = link.get_attribute("href")
#             if url and ("/p/" in url or "/reel/" in url):
#                 post = {"url": url, "image_url": None, "timestamp": None}
#                 break  # Only take the first/latest post
#     except Exception as e:
#         print(f"⚠️ Error finding post URL: {e}")

#     if post:
#         driver.get(post["url"])
#         time.sleep(5)

#         # --- Extract Post Image ---
#         try:
#             image_element = driver.find_element(By.XPATH, "//div[contains(@class, '_aagv')]/img")
#             post["image_url"] = image_element.get_attribute("src")
#             print(f"✅ Post Image URL: {post['image_url']}")
#         except Exception as e:
#             print(f"⚠️ Could not fetch post image: {e}")

#         # --- Extract Timestamp ---
#         try:
#             time_element = driver.find_element(By.TAG_NAME, "time")
#             ts_str = time_element.get_attribute("datetime")
#             if ts_str:
#                 utc_time = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
#                 post["timestamp"] = utc_time.astimezone(timezone(timedelta(hours=5)))  # Convert to Pakistan Time (UTC+5)
#         except Exception as e:
#             print(f"⚠️ Could not get timestamp for {post['url']}: {e}")

#     driver.quit()
#     return post

# # --- Upload Post Image to Cloudinary ---
# def upload_to_cloudinary(image_url, page_name):
#     response = requests.get(image_url, stream=True)
#     if response.status_code == 200:
#         cloud_response = cloudinary.uploader.upload(response.raw, folder="instagram_posts", public_id=page_name)
#         return cloud_response["secure_url"]
#     return None

# # --- Scrape & Store Data in PostgreSQL ---
# def scrape_instagram():
#     conn = psycopg2.connect(DATABASE_URL)
#     cursor = conn.cursor()
    
#     # Create table if not exists
#     create_table_query = """
#     CREATE TABLE IF NOT EXISTS instagram_posts (
#         id SERIAL PRIMARY KEY,
#         page_name TEXT NOT NULL,
#         link TEXT NOT NULL UNIQUE,
#         post_image TEXT,
#         timestamp TIMESTAMP
#     );
#     """
#     cursor.execute(create_table_query)
#     conn.commit()

#     for page_name, page_url in INSTAGRAM_PAGES.items():
#         print(f"🔍 Scraping Instagram page: {page_name}")
#         post = get_instagram_post(page_url)

#         if post and post["image_url"]:
#             print(f"✅ Latest Post: {post['url']} | Image: {post['image_url']} | timestamp: {post["timestamp"]}")

#             # Upload post image to Cloudinary
#             cloudinary_url = upload_to_cloudinary(post["image_url"], page_name)

#             # Insert into DB only if new post is found
#             cursor.execute("SELECT link FROM instagram_posts WHERE page_name = %s ORDER BY timestamp DESC LIMIT 1", (page_name,))
#             result = cursor.fetchone()

#             if result and result[0] != post["url"]:
#                 print(f"🔄 Updating {page_name} with new post...")
#                 cursor.execute(
#                     "INSERT INTO instagram_posts (page_name, link, post_image, timestamp) VALUES (%s, %s, %s, %s)",
#                     (page_name, post["url"], cloudinary_url, post["timestamp"])
#                 )
#             elif not result:
#                 print(f"🆕 Adding first post for {page_name}...")
#                 cursor.execute(
#                     "INSERT INTO instagram_posts (page_name, link, post_image, timestamp) VALUES (%s, %s, %s, %s)",
#                     (page_name, post["url"], cloudinary_url, post["timestamp"])
#                 )

#             conn.commit()
#         else:
#             print(f"❌ No new post found for {page_name}")

#     cursor.close()
#     conn.close()
#     print("✅ Instagram scraping complete!")

# # --- Main Loop ---
# while True:
#     scrape_instagram()
#     print("⏳ Waiting 30 minutes before next scrape...")
#     time.sleep(60 * 30)












































# import time
# import pickle
# import psycopg2
# import requests
# import cloudinary
# import cloudinary.uploader
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from datetime import datetime, timezone, timedelta

# # --- PostgreSQL Database ---
# DATABASE_URL = "postgresql://instaxrss_user:QGBb5ALqiBraZtjt1c1zoifa4Kf4G1Tu@dpg-cv7sqcqj1k6c739htp00-a.oregon-postgres.render.com/instaxrss"

# # --- Cloudinary Configuration ---
# cloudinary.config(
#     cloud_name="dka67k5av",
#     api_key="696938932641642",
#     api_secret="Ow7AilWBHGJnkotnC_YVR6xVa6M"
# )

# # --- Selenium WebDriver Setup ---
# insta_options = Options()
# insta_options.add_argument("--headless=new")
# insta_options.add_argument("--disable-gpu")
# insta_options.add_argument("--window-size=375,812")
# insta_options.add_argument("--disable-blink-features=AutomationControlled")
# insta_options.add_argument(
#     "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) "
#     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Mobile Safari/537.36"
# )

# INSTAGRAM_PAGES = {
#     "Kim Kardashian": "https://www.instagram.com/kimkardashian/",
#     "Kylie Jenner": "https://www.instagram.com/kyliejenner/",
#     "Rihanna": "https://www.instagram.com/badgalriri/",
#     "Kanye West": "https://www.instagram.com/ye/",
#     "Justin Bieber": "https://www.instagram.com/justinbieber/",
#     "Hailey Bieber": "https://www.instagram.com/haileybieber/",
#     "Selena Gomez": "https://www.instagram.com/selenagomez/",
#     "Henry Cavill": "https://www.instagram.com/HenryCavill/",
#     "Emma Roberts": "https://www.instagram.com/emmaroberts/",
#     "Reese Witherspoon": "https://www.instagram.com/reesewitherspoon/",
#     "Shakira": "https://www.instagram.com/shakira/",
#     "Beyoncé": "https://www.instagram.com/beyonce/",
#     "Lady Gaga": "https://www.instagram.com/ladygaga/",
#     "Ariana Grande": "https://www.instagram.com/arianagrande/",
#     "Billie Eilish": "https://www.instagram.com/billieeilish/",
#     "Miley Cyrus": "https://www.instagram.com/mileycyrus/",
#     "Taylor Swift": "https://www.instagram.com/taylorswift/",
#     "Gigi Hadid": "https://www.instagram.com/gigihadid/",
#     "Zayn Malik": "https://www.instagram.com/zayn/",
#     "Tom Cruise": "https://www.instagram.com/tomcruise/",
#     "Barry Keoghan": "https://www.instagram.com/barrykeoghansource/",
#     "Meghan Markle": "https://www.instagram.com/meghan/",
#     "Kendall Jenner": "https://www.instagram.com/kendalljenner/",
#     "Kris Jenner": "https://www.instagram.com/krisjenner/",
#     "Khloé Kardashian": "https://www.instagram.com/khloekardashian/",
#     "Kourtney Kardashian": "https://www.instagram.com/kourtneykardash/",
#     "Jeremy Renner": "https://www.instagram.com/jeremyrenner/?hl=en",
#     "Chris Hemsworth": "https://www.instagram.com/chrishemsworth/",
#     "Ed Sheeran": "https://www.instagram.com/teddysphotos/",
#     "Sydney Sweeney": "https://www.instagram.com/sydney_sweeney/",
#     "Anne Hathaway": "https://www.instagram.com/annehathaway/",
#     "Jennifer Lopez": "https://www.instagram.com/jlo/",
#     "Jennifer Garner": "https://www.instagram.com/jennifer.garner/",
#     "Jennifer Aniston": "https://www.instagram.com/jenniferaniston/",
#     "Jennifer Lawrence": "https://www.instagram.com/1jnnf/",
#     "Meghan Markle": "https://www.instagram.com/meghan/",
#     "The Royal Family": "https://www.instagram.com/theroyalfamily/",
#     "Cardi B": "https://www.instagram.com/iamcardib/",
#     "Soompi": "https://www.instagram.com/soompi/",
#     "Katy Perry": "https://www.instagram.com/katyperry/",
#     "Paris Hilton": "https://www.instagram.com/parishilton/",
#     "Zendaya": "https://www.instagram.com/zendaya/",
#     "Jenna Ortega": "https://www.instagram.com/jennaortega/",
#     "Netflix": "https://www.instagram.com/netflix/",
#     "Tom Hanks": "https://www.instagram.com/tomhanks/",
#     "Vin Diesel": "https://www.instagram.com/vindiesel/",
#     "Robert Downey Jr.": "https://www.instagram.com/robertdowneyjr/"
# }

# # --- Load Instagram Cookies ---
# def load_cookies(driver, file_path):
#     try:
#         cookies = pickle.load(open(file_path, "rb"))
#         for cookie in cookies:
#             driver.add_cookie(cookie)
#         print(f"✅ Cookies loaded from {file_path}!")
#     except Exception as e:
#         print(f"⚠️ Error loading cookies from {file_path}: {e}")

# # --- Extract Latest Post Data ---
# def get_instagram_post(page_url):
#     driver = webdriver.Chrome(options=insta_options)
#     driver.get("https://www.instagram.com/")
#     time.sleep(5)

#     load_cookies(driver, "instagram_cookies.pkl")
#     driver.refresh()
#     time.sleep(5)

#     driver.get(page_url)
#     time.sleep(10)

#     post = None

#     # --- Extract Latest Post URL ---
#     try:
#         post_links = driver.find_elements(By.TAG_NAME, "a")
#         for link in post_links:
#             url = link.get_attribute("href")
#             if url and ("/p/" in url or "/reel/" in url):
#                 post = {"url": url, "image_url": None, "timestamp": None, "caption": ""}
#                 break
#     except Exception as e:
#         print(f"⚠️ Error finding post URL: {e}")

#     if post:
#         driver.get(post["url"])
#         time.sleep(5)

#         # --- Extract Post Image ---
#         try:
#             image_element = driver.find_element(By.XPATH, "//div[contains(@class, '_aagv')]/img")
#             post["image_url"] = image_element.get_attribute("src")
#             print(f"✅ Post Image URL: {post['image_url']}")
#         except Exception as e:
#             print(f"⚠️ Could not fetch post image: {e}")

#         # --- Extract Caption ---
#         try:
#             # caption_element = driver.find_element(By.XPATH, "//div[contains(@class, 'xt0psk2')]/h1")
#             # post["caption"] = caption_element.text
#             # print("Post Caption:", post["caption"])


#             caption_element = driver.find_element(By.XPATH, "//h1[contains(@class, '_ap3a _aaco _aacu _aacx _aad7 _aade')]")
#             post["caption"] = str(caption_element.text)
#             print("Post Caption:", post["caption"])


#             # caption_element = driver.find_element(By.XPATH, "//h1[contains(@class, '_ap3a _aaco _aacu _aacx _aad7 _aade')]")
#             # post["caption"] = caption_element.text.encode("utf-8", "ignore").decode("utf-8")  # Encode & Decode to remove encoding issues
#             # print("Post Caption:", post["caption"])
#         except Exception as e:
#             print(f"⚠️ Could not fetch post caption: {e}")

#         # --- Extract Timestamp ---
#         try:
#             time_element = driver.find_element(By.TAG_NAME, "time")
#             ts_str = time_element.get_attribute("datetime")
#             if ts_str:
#                 utc_time = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
#                 post["timestamp"] = utc_time.astimezone(timezone(timedelta(hours=5)))  # Convert to Pakistan Time (UTC+5)
#         except Exception as e:
#             print(f"⚠️ Could not get timestamp for {post['url']}: {e}")

#     driver.quit()
#     return post

# # --- Upload Post Image to Cloudinary ---
# def upload_to_cloudinary(image_url, page_name):
#     response = requests.get(image_url, stream=True)
#     if response.status_code == 200:
#         cloud_response = cloudinary.uploader.upload(response.raw, folder="instagram_posts", public_id=page_name)
#         return cloud_response["secure_url"]
#     return None

# # --- Scrape & Store Data in PostgreSQL ---
# def scrape_instagram():
#     conn = psycopg2.connect(DATABASE_URL)
#     cursor = conn.cursor()
    
#     # Create table if not exists
#     create_table_query = """
#     CREATE TABLE IF NOT EXISTS instagram_posts (
#         id SERIAL PRIMARY KEY,
#         page_name TEXT NOT NULL,
#         link TEXT NOT NULL UNIQUE,
#         post_image TEXT,
#         caption TEXT,
#         timestamp TIMESTAMP
#     );
#     """
#     cursor.execute(create_table_query)
#     conn.commit()

#     for page_name, page_url in INSTAGRAM_PAGES.items():
#         print(f"🔍 Scraping Instagram page: {page_name}")
#         post = get_instagram_post(page_url)

#         if post and post["image_url"]:
#             print(f"✅ Latest Post: {post['url']} | Image: {post['image_url']} | Caption: {post['caption']}")

#             # Upload post image to Cloudinary
#             cloudinary_url = upload_to_cloudinary(post["image_url"], page_name)

#             # Insert into DB only if new post is found
#             cursor.execute("SELECT link FROM instagram_posts WHERE page_name = %s ORDER BY timestamp DESC LIMIT 1", (page_name,))
#             result = cursor.fetchone()

#             if result and result[0] != post["url"]:
#                 print(f"🔄 Updating {page_name} with new post...")
#                 cursor.execute(
#                      """INSERT INTO instagram_posts (page_name, link, post_image, timestamp, caption)
#                         VALUES (%s, %s, %s, %s, %s)
#                         ON CONFLICT (link) 
#                         DO UPDATE SET post_image = EXCLUDED.post_image, timestamp = EXCLUDED.timestamp, caption = EXCLUDED.caption""",
#                         (page_name, post["url"], cloudinary_url, post["timestamp"], post["caption"] or "No caption")
#                 )
#             elif not result:
#                 print(f"🆕 Adding first post for {page_name}...")
#                 cursor.execute(
#                     "INSERT INTO instagram_posts (page_name, link, post_image, caption, timestamp) VALUES (%s, %s, %s, %s, %s)",
#                     (page_name, post["url"], cloudinary_url, post["caption"], post["timestamp"])
#                 )

#             conn.commit()
#         else:
#             print(f"❌ No new post found for {page_name}")

#     cursor.close()
#     conn.close()
#     print("✅ Instagram scraping complete!")
# scrape_instagram()
# # --- Main Loop ---
# # while True:
    
#     # print("⏳ Waiting 30 minutes before next scrape...")
#     # time.sleep(60 * 30)





# ------------------------------------------------------------working good but extracting image url of all four posts

# import time
# import pickle
# import psycopg2
# import requests
# import cloudinary
# import cloudinary.uploader
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from datetime import datetime, timezone, timedelta

# # --- PostgreSQL Database ---
# DATABASE_URL = "postgresql://instaxrss_user:QGBb5ALqiBraZtjt1c1zoifa4Kf4G1Tu@dpg-cv7sqcqj1k6c739htp00-a.oregon-postgres.render.com/instaxrss"

# # --- Cloudinary Configuration ---
# cloudinary.config(
#     cloud_name="dka67k5av",
#     api_key="696938932641642",
#     api_secret="Ow7AilWBHGJnkotnC_YVR6xVa6M"
# )

# # --- Selenium WebDriver Setup ---
# insta_options = Options()
# insta_options.add_argument("--headless=new")
# insta_options.add_argument("--disable-gpu")
# insta_options.add_argument("--window-size=375,812")
# insta_options.add_argument("--disable-blink-features=AutomationControlled")
# insta_options.add_argument(
#     "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) "
#     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Mobile Safari/537.36"
# )

# # --- Instagram Pages ---
# INSTAGRAM_PAGES = {
#     "Billie Eilish": "https://www.instagram.com/billieeilish/"

#     # Add more pages as needed
# }

# # --- Load Instagram Cookies ---
# def load_cookies(driver, file_path):
#     try:
#         cookies = pickle.load(open(file_path, "rb"))
#         for cookie in cookies:
#             driver.add_cookie(cookie)
#         print(f"✅ Cookies loaded from {file_path}!")
#     except Exception as e:
#         print(f"⚠️ Error loading cookies from {file_path}: {e}")

# # --- Extract Latest Post Data (excluding pinned posts) ---
# def get_latest_instagram_post(page_url):
#     driver = webdriver.Chrome(options=insta_options)
#     driver.get("https://www.instagram.com/")
#     time.sleep(5)

#     load_cookies(driver, "instagram_cookies.pkl")
#     driver.refresh()
#     time.sleep(5)

#     driver.get(page_url)
#     time.sleep(10)

#     posts = []
#     # Gather several candidate post URLs from the page
#     links = driver.find_elements(By.TAG_NAME, "a")
#     for link in links:
#         url = link.get_attribute("href")
#         if url and ("/p/" in url or "/reel/" in url):
#             # Initialize post data dictionary
#             posts.append({
#                 "url": url,
#                 "timestamp": None,
#                 "image_url": None,
#                 "caption": "",
#                 "is_pinned": False
#             })
#             if len(posts) == 4:  # Collect a few candidates to filter out pinned posts
#                 break

#     # Visit each candidate to extract details and check for pinned indicator
#     for post in posts:
#         driver.get(post["url"])
#         time.sleep(5)

#         # Check for pinned label (if found, mark as pinned and skip detail extraction)
#         try:
#             pinned_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Pinned')]")
#             if pinned_element:
#                 post["is_pinned"] = True
#                 print(f"🔖 Skipping pinned post: {post['url']}")
#                 continue
#         except Exception:
#             post["is_pinned"] = False

#         # Extract timestamp
#         try:
#             time_element = driver.find_element(By.TAG_NAME, "time")
#             ts_str = time_element.get_attribute("datetime")
#             if ts_str:
#                 post["timestamp"] = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
#         except Exception as e:
#             print(f"⚠️ Could not get timestamp for {post['url']}: {e}")
#             post["timestamp"] = None

#         # Extract post image URL
#         try:
#             image_element = driver.find_element(By.XPATH, "//div[contains(@class, '_aagv')]/img")
#             post["image_url"] = image_element.get_attribute("src")
#             # print(f"✅ Post Image URL: {post['image_url']}")
#         except Exception as e:
#             print(f"⚠️ Could not fetch image for {post['url']}: {e}")

#         # Extract caption (if available)
#         try:
#             caption_element = driver.find_element(By.XPATH, "//h1[contains(@class, '_ap3a _aaco _aacu _aacx _aad7 _aade')]")
#             post["caption"] = caption_element.text
#             # print(f"📝 Post Caption: {post['caption']}")
#         except Exception as e:
#             print(f"⚠️ Could not fetch caption for {post['url']}: {e}")

#     driver.quit()

#     # Filter out posts that have no timestamp or are pinned
#     valid_posts = [p for p in posts if p["timestamp"] and not p["is_pinned"]]
#     if valid_posts:
#         latest_post = max(valid_posts, key=lambda p: p["timestamp"])
#         # print(f"👉 Latest non-pinned post selected: {latest_post['url']}")
#         return latest_post
#     else:
#         print("❌ No valid (non-pinned) post found.")
#         return None

# # --- Upload Post Image to Cloudinary ---
# def upload_to_cloudinary(image_url, page_name):
#     response = requests.get(image_url, stream=True)
#     if response.status_code == 200:
#         cloud_response = cloudinary.uploader.upload(response.raw, folder="instagram_post", public_id=page_name)
#         return cloud_response["secure_url"]
#     return None

# # --- Scrape & Store Data in PostgreSQL ---
# def scrape_instagram():
#     conn = psycopg2.connect(DATABASE_URL)
#     cursor = conn.cursor()
    
#     # Create table if it does not exist
#     create_table_query = """
#     CREATE TABLE IF NOT EXISTS instagram_post (
#         id SERIAL PRIMARY KEY,
#         page_name TEXT NOT NULL,
#         link TEXT NOT NULL UNIQUE,
#         post_image TEXT,
#         caption TEXT,
#         timestamp TIMESTAMP
#     );
#     """
#     cursor.execute(create_table_query)
#     conn.commit()

#     for page_name, page_url in INSTAGRAM_PAGES.items():
#         print(f"🔍 Scraping Instagram page: {page_name}")
#         post = get_latest_instagram_post(page_url)

#         if post and post["image_url"]:
#             print(f"✅ Latest Post: {post['url']}\n   Image: {post['image_url']}\n   Caption: {post['caption']}\n   Timestamp: {post['timestamp']}")
#             # Upload image to Cloudinary
#             cloudinary_url = upload_to_cloudinary(post["image_url"], page_name)
            
#             # Insert or update post in the database based on uniqueness of the link
#             cursor.execute("SELECT link FROM instagram_post WHERE page_name = %s ORDER BY timestamp DESC LIMIT 1", (page_name,))
#             result = cursor.fetchone()

#             if result and result[0] != post["url"]:
#                 print(f"🔄 Updating {page_name} with new post...")
#                 cursor.execute(
#                      """INSERT INTO instagram_post (page_name, link, post_image, timestamp, caption)
#                         VALUES (%s, %s, %s, %s, %s)
#                         ON CONFLICT (link) 
#                         DO UPDATE SET post_image = EXCLUDED.post_image, timestamp = EXCLUDED.timestamp, caption = EXCLUDED.caption""",
#                         (page_name, post["url"], cloudinary_url, post["timestamp"], post["caption"] or "No caption")
#                 )
#             elif not result:
#                 print(f"🆕 Adding first post for {page_name}...")
#                 cursor.execute(
#                     "INSERT INTO instagram_post (page_name, link, post_image, caption, timestamp) VALUES (%s, %s, %s, %s, %s)",
#                     (page_name, post["url"], cloudinary_url, post["caption"], post["timestamp"])
#                 )
#             conn.commit()
#         else:
#             print(f"❌ No new (non-pinned) post found for {page_name}")

#     cursor.close()
#     conn.close()
#     print("✅ Instagram scraping complete!")

# # Run the scraping once (or uncomment the loop below for periodic scraping)
# scrape_instagram()

# # --- Main Loop for periodic scraping ---
# # while True:
# #     scrape_instagram()
# #     print("⏳ Waiting 30 minutes before next scrape...")
# #     time.sleep(60 * 30)


























# import time
# import pickle
# import psycopg2
# import requests
# import cloudinary
# import cloudinary.uploader
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from datetime import datetime

# # --- PostgreSQL Database ---
# DATABASE_URL = "postgresql://instaxrss_user:QGBb5ALqiBraZtjt1c1zoifa4Kf4G1Tu@dpg-cv7sqcqj1k6c739htp00-a.oregon-postgres.render.com/instaxrss"

# # --- Cloudinary Configuration ---
# cloudinary.config(
#     cloud_name="dka67k5av",
#     api_key="696938932641642",
#     api_secret="Ow7AilWBHGJnkotnC_YVR6xVa6M"
# )

# # --- Selenium WebDriver Setup ---
# insta_options = Options()
# insta_options.add_argument("--headless=new")
# insta_options.add_argument("--disable-gpu")
# insta_options.add_argument("--window-size=375,812")
# insta_options.add_argument("--disable-blink-features=AutomationControlled")
# insta_options.add_argument(
#     "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) "
#     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Mobile Safari/537.36"
# )

# # --- Instagram Pages ---
# INSTAGRAM_PAGES = {
#     "Ariana Grande": "https://www.instagram.com/arianagrande/",
#     "Billie Eilish": "https://www.instagram.com/billieeilish/",
#     "Kim Kardashian": "https://www.instagram.com/kimkardashian/"
#     # Add more pages as needed
# }

# # --- Load Instagram Cookies ---
# def load_cookies(driver, file_path):
#     try:
#         cookies = pickle.load(open(file_path, "rb"))
#         for cookie in cookies:
#             driver.add_cookie(cookie)
#         print(f"✅ Cookies loaded from {file_path}!")
#     except Exception as e:
#         print(f"⚠️ Error loading cookies from {file_path}: {e}")

# # --- Extract Latest Post Data (extract timestamp & pinned flag from candidates, then get image & caption only from latest candidate) ---
# def get_latest_instagram_post(page_url):
#     driver = webdriver.Chrome(options=insta_options)
#     driver.get("https://www.instagram.com/")
#     time.sleep(5)

#     load_cookies(driver, "instagram_cookies.pkl")
#     driver.refresh()
#     time.sleep(5)

#     driver.get(page_url)
#     time.sleep(10)

#     # Collect candidate post URLs (up to 4)
#     candidate_urls = []
#     links = driver.find_elements(By.TAG_NAME, "a")
#     for link in links:
#         url = link.get_attribute("href")
#         if url and ("/p/" in url or "/reel/" in url):
#             candidate_urls.append(url)
#             if len(candidate_urls) == 4:
#                 break

#     # For each candidate, extract only timestamp and check pinned flag.
#     candidate_data = []
#     for url in candidate_urls:
#         driver.get(url)
#         time.sleep(5)
#         is_pinned = False
#         try:
#             pinned_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Pinned')]")
#             if pinned_element:
#                 is_pinned = True
#                 print(f"🔖 Skipping pinned candidate: {url}")
#         except Exception:
#             is_pinned = False

#         timestamp = None
#         try:
#             time_element = driver.find_element(By.TAG_NAME, "time")
#             ts_str = time_element.get_attribute("datetime")
#             if ts_str:
#                 timestamp = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
#         except Exception as e:
#             print(f"⚠️ Could not get timestamp for {url}: {e}")

#         candidate_data.append({
#             "url": url,
#             "timestamp": timestamp,
#             "is_pinned": is_pinned
#         })

#     # Filter out candidates that are pinned or have no timestamp
#     valid_candidates = [c for c in candidate_data if c["timestamp"] and not c["is_pinned"]]

#     if not valid_candidates:
#         driver.quit()
#         print("❌ No valid (non-pinned) post found.")
#         return None

#     # Select the latest candidate based on timestamp
#     latest_candidate = max(valid_candidates, key=lambda c: c["timestamp"])
#     print(f"👉 Latest candidate selected: {latest_candidate['url']}")

#     # -----------------------------------Now extract the image URL and caption from the chosen candidate.
#     # driver.get(latest_candidate["url"])
#     # time.sleep(5)
#     # image_url = None
#     # caption = ""
#     # try:
#     #     image_element = driver.find_element(By.XPATH, "//div[contains(@class, '_aagv')]/img")
#     #     image_url = image_element.get_attribute("src")
#     # except Exception as e:
#     #     print(f"⚠️ Could not fetch image for {latest_candidate['url']}: {e}")

#     # try:
#     #     caption_element = driver.find_element(By.XPATH, "//h1[contains(@class, '_ap3a _aaco _aacu _aacx _aad7 _aade')]")
#     #     caption = caption_element.text
#     # except Exception as e:
#     #     print(f"⚠️ Could not fetch caption for {latest_candidate['url']}: {e}")

#     # driver.quit()

#     # # Combine the data and return
#     # return {
#     #     "url": latest_candidate["url"],
#     #     "timestamp": latest_candidate["timestamp"],
#     #     "image_url": image_url,
#     #     "caption": caption
#     # }
#     # --------------------------------------------------------------
#     driver.get(latest_candidate["url"])
#     time.sleep(5)

#     image_url = None
   
#     caption = ""

# # Check if it's a reel by looking for '/reel/' in the URL
#     if '/reel/' in latest_candidate["url"]:
#         try:
#         # For reels/videos, try extracting the thumbnail via the 'poster' attribute from the video element
#             image_element = driver.find_element(By.XPATH, "//div[contains(@class, '_aatk _aatn')]//video")
#             image_url = image_element.get_attribute("src")


#         except Exception as e:
#             print(f"⚠️ Could not fetch poster image for reel {latest_candidate['url']}: {e}")
#     else:
#         try:
#         # For regular image posts, extract the image URL from the expected <img> element
#             image_element = driver.find_element(By.XPATH, "//div[contains(@class, '_aagv')]/img")
#             image_url = image_element.get_attribute("src")
#         except Exception as e:
#             print(f"⚠️ Could not fetch image for {latest_candidate['url']}: {e}")

#         try:
#             caption_element = driver.find_element(By.XPATH, "//h1[contains(@class, '_ap3a _aaco _aacu _aacx _aad7 _aade')]")
#             caption = caption_element.text
#         except Exception as e:
#             print(f"⚠️ Could not fetch caption for {latest_candidate['url']}: {e}")

#     driver.quit()

# # Combine the data and return
#     return {
#         "url": latest_candidate["url"],
#         "timestamp": latest_candidate["timestamp"],
#         "image_url": image_url,
#         "caption": caption
# }





# # def upload_to_cloudinary(image_url, page_name):
# #     response = requests.get(image_url, stream=True)
# #     if response.status_code == 200:
# #         cloud_response = cloudinary.uploader.upload(response.raw, folder="instagram_posts", public_id=page_name)
# #         return cloud_response["secure_url"]
# #     return None



# # def upload_to_cloudinary(image_url, page_name):
# #     if ".mp4" in image_url:
# #         return image_url  # Return video URL as is

# #     response = requests.get(image_url)
# #     print(f"Status Code: {response.status_code}")  # Debugging
# #     print(f"Content-Type: {response.headers.get('Content-Type')}")  # Debugging

# #     if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
# #         cloud_response = cloudinary.uploader.upload(response.raw, folder="instagram_post", public_id=page_name)
# #         return cloud_response["secure_url"]
# #     return None  # Image not accessible or invalid




# def upload_to_cloudinary(image_url, page_name):
#     if ".mp4" in image_url:
#         return image_url  # Return video URL as is

#     response = requests.get(image_url)
#     print(f"Status Code: {response.status_code}")  # Debugging
#     print(f"Content-Type: {response.headers.get('Content-Type')}")  # Debugging

#     if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
#         cloud_response = cloudinary.uploader.upload(response.content, folder="instagram_post", public_id=page_name)
#         return cloud_response["secure_url"]
#     return None  # Image not accessible or invalid

# # Test URLs
# image_url = "https://instagram.fkhi30-1.fna.fbcdn.net/v/t51.2885-15/484304334_18567681004047811_5924328281592061048_n.jpg?stp=dst-jpg_e35_p480x480_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6ImltYWdlX3VybGdlbi4xMjU2eDE1NzAuc2RyLmY3NTc2MS5kZWZhdWx0X2ltYWdlIn0&_nc_ht=instagram.fkhi30-1.fna.fbcdn.net&_nc_cat=1&_nc_oc=Q6cZ2QHhPtpvT-UkUsWI19tzkOSiSI3vnjNg_d15NQMgTns-clFeT0FX8v94n2YUNgO9nGQ&_nc_ohc=W1BDBu3JjdYQ7kNvgEGnzcm&_nc_gid=JAoFrl9TqPQJcscKIYyUAQ&edm=ALQROFkBAAAA&ccb=7-5&ig_cache_key=MzU4Njk2ODk1NDgwMTMyNzkyNg%3D%3D.3-ccb7-5&oh=00_AYE9yjFGIVBn4-NkBKUhRVCEUTWEqbdhKPYaa-v2K1pfbA&oe=67E02AF3&_nc_sid=fc8dfb"
# video_url = "https://instagram.fkhi30-1.fna.fbcdn.net/xyz.mp4"

# print(upload_to_cloudinary(image_url, "example_page"))
# print(upload_to_cloudinary(video_url, "example_page"))





# # --- Scrape & Store Data in PostgreSQL ---
# def scrape_instagram():
#     conn = psycopg2.connect(DATABASE_URL)
#     cursor = conn.cursor()
    
#     # Create table if it does not exist
#     create_table_query = """
#     CREATE TABLE IF NOT EXISTS instagram_post (
#         id SERIAL PRIMARY KEY,
#         page_name TEXT NOT NULL,
#         link TEXT NOT NULL UNIQUE,
#         post_image TEXT,
#         caption TEXT,
#         timestamp TIMESTAMP
#     );
#     """
#     cursor.execute(create_table_query)
#     conn.commit()

#     for page_name, page_url in INSTAGRAM_PAGES.items():
#         print(f"🔍 Scraping Instagram page: {page_name}")
#         post = get_latest_instagram_post(page_url)

#         if post and post["image_url"]:
#             print(f"✅ Latest Post: {post['url']}\n   Image: {post['image_url']}\n   Caption: {post['caption']}\n   Timestamp: {post['timestamp']}")
#             # Upload image to Cloudinary
#             cloudinary_url = upload_to_cloudinary(post["image_url"], page_name)
            
#             # Insert or update post in the database based on uniqueness of the link
#             cursor.execute("SELECT link FROM instagram_post WHERE page_name = %s ORDER BY timestamp DESC LIMIT 1", (page_name,))
#             result = cursor.fetchone()

#             if result and result[0] != post["url"]:
#                 print(f"🔄 Updating {page_name} with new post...")
#                 cursor.execute(
#                      """INSERT INTO instagram_post (page_name, link, post_image, timestamp, caption)
#                         VALUES (%s, %s, %s, %s, %s)
#                         ON CONFLICT (link) 
#                         DO UPDATE SET post_image = EXCLUDED.post_image, timestamp = EXCLUDED.timestamp, caption = EXCLUDED.caption""",
#                         (page_name, post["url"], cloudinary_url, post["timestamp"], post["caption"] or "No caption")
#                 )
#             elif not result:
#                 print(f"🆕 Adding first post for {page_name}...")
#                 cursor.execute(
#                     "INSERT INTO instagram_post (page_name, link, post_image, caption, timestamp) VALUES (%s, %s, %s, %s, %s)",
#                     (page_name, post["url"], cloudinary_url, post["caption"], post["timestamp"])
#                 )
#             conn.commit()
#         else:
#             print(f"❌ No valid (non-pinned) post found for {page_name}")

#     cursor.close()
#     conn.close()
#     print("✅ Instagram scraping complete!")

# # Run the scraping once (or uncomment the loop below for periodic scraping)
# scrape_instagram()

# # --- Main Loop for periodic scraping ---
# # while True:
# #     scrape_instagram()
# #     print("⏳ Waiting 30 minutes before next scrape...")
# #     time.sleep(60 * 30)




























#---------------------------------------------different columns for post and videos


# import time
# import pickle
# import psycopg2
# import requests
# import cloudinary
# import cloudinary.uploader
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from datetime import datetime

# # --- PostgreSQL Database ---
# DATABASE_URL = "postgresql://instaxrss_user:QGBb5ALqiBraZtjt1c1zoifa4Kf4G1Tu@dpg-cv7sqcqj1k6c739htp00-a.oregon-postgres.render.com/instaxrss"

# # --- Cloudinary Configuration ---
# cloudinary.config(
#     cloud_name="dka67k5av",
#     api_key="696938932641642",
#     api_secret="Ow7AilWBHGJnkotnC_YVR6xVa6M"
# )

# # --- Selenium WebDriver Setup ---
# insta_options = Options()
# insta_options.add_argument("--headless=new")
# insta_options.add_argument("--disable-gpu")
# insta_options.add_argument("--window-size=375,812")
# insta_options.add_argument("--disable-blink-features=AutomationControlled")
# insta_options.add_argument(
#     "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) "
#     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Mobile Safari/537.36"
# )

# # --- Instagram Pages ---
# INSTAGRAM_PAGES = {
#     "Ariana Grande": "https://www.instagram.com/arianagrande/"
#     # "Billie Eilish": "https://www.instagram.com/billieeilish/",
#     # "Kim Kardashian": "https://www.instagram.com/kimkardashian/"
# }

# # --- Load Instagram Cookies ---
# def load_cookies(driver, file_path):
#     try:
#         cookies = pickle.load(open(file_path, "rb"))
#         for cookie in cookies:
#             driver.add_cookie(cookie)
#         print(f"✅ Cookies loaded from {file_path}!")
#     except Exception as e:
#         print(f"⚠️ Error loading cookies from {file_path}: {e}")

# # --- Extract Latest Post Data ---
# def get_latest_instagram_post(page_url):
#     driver = webdriver.Chrome(options=insta_options)
#     driver.get("https://www.instagram.com/")
#     time.sleep(5)
#     load_cookies(driver, "instagram_cookies.pkl")
#     driver.refresh()
#     time.sleep(5)
#     driver.get(page_url)
#     time.sleep(10)

#     candidate_urls = []
#     for link in driver.find_elements(By.TAG_NAME, "a"):
#         url = link.get_attribute("href")
#         if url and ("/p/" in url or "/reel/" in url):
#             candidate_urls.append(url)
#             if len(candidate_urls) == 4:
#                 break

#     valid_candidates = []
#     for url in candidate_urls:
#         driver.get(url)
#         time.sleep(5)
        
#         is_pinned = bool(driver.find_elements(By.XPATH, "//*[contains(text(), 'Pinned')]") )
#         if is_pinned:
#             print(f"🔖 Skipping pinned candidate: {url}")
#             continue
        
#         timestamp = None
#         try:
#             ts_str = driver.find_element(By.TAG_NAME, "time").get_attribute("datetime")
#             timestamp = datetime.fromisoformat(ts_str.replace("Z", "+00:00")) if ts_str else None
#         except:
#             pass
        
#         if timestamp:
#             valid_candidates.append({"url": url, "timestamp": timestamp})

#     if not valid_candidates:
#         driver.quit()
#         print("❌ No valid (non-pinned) post found.")
#         return None

#     latest_candidate = max(valid_candidates, key=lambda c: c["timestamp"])
#     driver.get(latest_candidate["url"])
#     time.sleep(5)

#     image_url = None
#     video_url = None
#     caption = ""

#     if '/reel/' in latest_candidate["url"]:
#         try:
#             video_element = driver.find_element(By.XPATH, "//div[contains(@class, '_aatk _aatn')]//video")
#             video_url = video_element.get_attribute("src")
#         except:
#             pass
#     else:
#         try:
#             image_element = driver.find_element(By.XPATH, "//div[contains(@class, '_aagv')]/img")
#             image_url = image_element.get_attribute("src")
#         except:
#             pass
    
#     try:
#         caption = driver.find_element(By.XPATH, "//h1[contains(@class, '_ap3a')]").text
#     except:
#         pass

#     driver.quit()
#     return {
#         "url": latest_candidate["url"],
#         "timestamp": latest_candidate["timestamp"],
#         "image_url": image_url,
#         "video_url": video_url,
#         "caption": caption
#     }

# # --- Upload Image to Cloudinary ---
# def upload_to_cloudinary(image_url, page_name):
#     # if not image_url:
#     #     return None

#     if not image_url or "video" in image_url:
#         return image_url  # Return video URL as it is instead of None
#     response = requests.get(image_url)
#     if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
#         cloud_response = cloudinary.uploader.upload(response.content, folder="instagram_post", public_id=page_name)
#         return cloud_response["secure_url"]
#     return None

# # --- Scrape & Store Data in PostgreSQL ---
# def scrape_instagram():
#     conn = psycopg2.connect(DATABASE_URL)
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS instagram_post (
#             id SERIAL PRIMARY KEY,
#             page_name TEXT NOT NULL,
#             link TEXT NOT NULL UNIQUE,
#             post_image TEXT,
#             video_url TEXT,
#             caption TEXT,
#             timestamp TIMESTAMP
#         );
#     """)
#     conn.commit()

#     for page_name, page_url in INSTAGRAM_PAGES.items():
#         print(f"🔍 Scraping Instagram page: {page_name}")
#         post = get_latest_instagram_post(page_url)
#         if post:
#             cloudinary_url = upload_to_cloudinary(post["image_url"], page_name) if post["image_url"] else None
#             cursor.execute("""
#                 INSERT INTO instagram_post (page_name, link, post_image, video_url, caption, timestamp)
#                 VALUES (%s, %s, %s, %s, %s, %s)
#                 ON CONFLICT (link) 
#                 DO UPDATE SET post_image = EXCLUDED.post_image, video_url = EXCLUDED.video_url, 
#                 caption = EXCLUDED.caption, timestamp = EXCLUDED.timestamp
#             """, (page_name, post["url"], cloudinary_url, post["video_url"], post["caption"] or "No caption", post["timestamp"]))
#             conn.commit()
#     cursor.close()
#     conn.close()
#     print("✅ Instagram scraping complete!")

# scrape_instagram()

















# import time
# import pickle
# import psycopg2
# import requests
# import cloudinary
# import cloudinary.uploader
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from datetime import datetime

# # --- PostgreSQL Database ---
# DATABASE_URL = "postgresql://instaxrss_user:QGBb5ALqiBraZtjt1c1zoifa4Kf4G1Tu@dpg-cv7sqcqj1k6c739htp00-a.oregon-postgres.render.com/instaxrss"

# # --- Cloudinary Configuration ---
# cloudinary.config(
#     cloud_name="dka67k5av",
#     api_key="696938932641642",
#     api_secret="Ow7AilWBHGJnkotnC_YVR6xVa6M"
# )

# # --- Selenium WebDriver Setup ---
# insta_options = Options()
# insta_options.add_argument("--headless=new")
# insta_options.add_argument("--disable-gpu")
# insta_options.add_argument("--window-size=375,812")
# insta_options.add_argument("--disable-blink-features=AutomationControlled")
# insta_options.add_argument(
#     "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) "
#     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Mobile Safari/537.36"
# )

# # --- Instagram Pages ---
# INSTAGRAM_PAGES = {
#     "Kim Kardashian": "https://www.instagram.com/kimkardashian/",
#     "Kylie Jenner": "https://www.instagram.com/kyliejenner/",
#     "Rihanna": "https://www.instagram.com/badgalriri/",
#     "Kanye West": "https://www.instagram.com/ye/",
#     "Justin Bieber": "https://www.instagram.com/justinbieber/",
#     "Hailey Bieber": "https://www.instagram.com/haileybieber/",
#     "Selena Gomez": "https://www.instagram.com/selenagomez/",
#     "Henry Cavill": "https://www.instagram.com/HenryCavill/",
#     "Emma Roberts": "https://www.instagram.com/emmaroberts/",
#     "Reese Witherspoon": "https://www.instagram.com/reesewitherspoon/",
#     "Shakira": "https://www.instagram.com/shakira/",
#     "Beyoncé": "https://www.instagram.com/beyonce/",
#     "Lady Gaga": "https://www.instagram.com/ladygaga/",
#     "Ariana Grande": "https://www.instagram.com/arianagrande/",
#     "Billie Eilish": "https://www.instagram.com/billieeilish/",
#     "Miley Cyrus": "https://www.instagram.com/mileycyrus/",
#     # "Taylor Swift": "https://www.instagram.com/taylorswift/",
#     "Gigi Hadid": "https://www.instagram.com/gigihadid/",
#     "Zayn Malik": "https://www.instagram.com/zayn/",
#     "Tom Cruise": "https://www.instagram.com/tomcruise/",
#     "Barry Keoghan": "https://www.instagram.com/barrykeoghansource/",
#     "Meghan Markle": "https://www.instagram.com/meghan/",
#     "Kendall Jenner": "https://www.instagram.com/kendalljenner/",
#     "Kris Jenner": "https://www.instagram.com/krisjenner/",
#     "Khloé Kardashian": "https://www.instagram.com/khloekardashian/",
#     "Kourtney Kardashian": "https://www.instagram.com/kourtneykardash/",
#     "Jeremy Renner": "https://www.instagram.com/jeremyrenner/?hl=en",
#     "Chris Hemsworth": "https://www.instagram.com/chrishemsworth/",
#     "Ed Sheeran": "https://www.instagram.com/teddysphotos/",
#     "Sydney Sweeney": "https://www.instagram.com/sydney_sweeney/",
#     "Anne Hathaway": "https://www.instagram.com/annehathaway/",
#     "Jennifer Lopez": "https://www.instagram.com/jlo/",
#     "Jennifer Garner": "https://www.instagram.com/jennifer.garner/",
#     "Jennifer Aniston": "https://www.instagram.com/jenniferaniston/",
#     "Jennifer Lawrence": "https://www.instagram.com/1jnnf/",
#     # "Meghan Markle": "https://www.instagram.com/meghan/",
#     "The Royal Family": "https://www.instagram.com/theroyalfamily/",
#     "Cardi B": "https://www.instagram.com/iamcardib/",
#     "Soompi": "https://www.instagram.com/soompi/",
#     "Katy Perry": "https://www.instagram.com/katyperry/",
#     "Paris Hilton": "https://www.instagram.com/parishilton/",
#     "Zendaya": "https://www.instagram.com/zendaya/",
#     "Jenna Ortega": "https://www.instagram.com/jennaortega/",
#     "Netflix": "https://www.instagram.com/netflix/",
#     "Tom Hanks": "https://www.instagram.com/tomhanks/",
#     "Vin Diesel": "https://www.instagram.com/vindiesel/",
#     "Robert Downey Jr.": "https://www.instagram.com/robertdowneyjr/",
#     "Prince and Princess of Wales": "https://www.instagram.com/princeandprincessofwales",
#     "The Royal Family": "https://www.instagram.com/theroyalfamily",
#     "Sarah Ferguson": "https://www.instagram.com/sarahferguson15",
#     "Meghan": "https://www.instagram.com/meghan",
#     "Duke and Duchess of Sussex Daily": "https://www.instagram.com/dukeandduchessofsussexdaily",
#     "Rebecca English": "https://www.instagram.com/byrebeccaenglish",
#     "Taylor Swift": "https://www.instagram.com/taylorswift",
#     # "Selena Gomez": "https://www.instagram.com/selenagomez",
#     "Killatrav": "https://www.instagram.com/killatrav",
#     "Princess Eugenie": "https://www.instagram.com/princesseugenie",
#     "Ryan Reynolds": "https://www.instagram.com/vancityreynolds",
#     # "Kylie Jenner": "https://www.instagram.com/kyliejenner",
#     # "Kendall Jenner": "https://www.instagram.com/kendalljenner",
#     # "Kim Kardashian": "https://www.instagram.com/kimkardashian",
#     "Gigi Hadid": "https://www.instagram.com/gigihadid"
# }

# # --- Load Instagram Cookies ---
# def load_cookies(driver, file_path):
#     try:
#         cookies = pickle.load(open(file_path, "rb"))
#         for cookie in cookies:
#             driver.add_cookie(cookie)
#         print(f"✅ Cookies loaded from {file_path}!")
#     except Exception as e:
#         print(f"⚠️ Error loading cookies from {file_path}: {e}")

# # --- Extract Latest Post Data ---
# def get_latest_instagram_post(page_url):
#     driver = webdriver.Chrome(options=insta_options)
#     driver.get("https://www.instagram.com/")
#     time.sleep(5)
#     load_cookies(driver, "instagram_cookies.pkl")
#     driver.refresh()
#     time.sleep(5)
#     driver.get(page_url)
#     time.sleep(10)

#     candidate_urls = []
#     for link in driver.find_elements(By.TAG_NAME, "a"):
#         url = link.get_attribute("href")
#         if url and ("/p/" in url or "/reel/" in url):
#             candidate_urls.append(url)
#             if len(candidate_urls) == 4:
#                 break

#     valid_candidates = []
#     for url in candidate_urls:
#         driver.get(url)
#         time.sleep(5)

#         is_pinned = bool(driver.find_elements(By.XPATH, "//*[contains(text(), 'Pinned')]"))
#         if is_pinned:
#             print(f"🔖 Skipping pinned post: {url}")
#             continue

#         timestamp = None
#         try:
#             ts_str = driver.find_element(By.TAG_NAME, "time").get_attribute("datetime")
#             timestamp = datetime.fromisoformat(ts_str.replace("Z", "+00:00")) if ts_str else None
#         except:
#             pass

#         if timestamp:
#             valid_candidates.append({"url": url, "timestamp": timestamp})

#     if not valid_candidates:
#         driver.quit()
#         print("❌ No valid (non-pinned) post found.")
#         return None

#     latest_candidate = max(valid_candidates, key=lambda c: c["timestamp"])
#     driver.get(latest_candidate["url"])
#     time.sleep(5)

#     post_image = None  # Store either image or video URL
#     caption = ""

#     if '/reel/' in latest_candidate["url"]:
#         try:
#             video_element = driver.find_element(By.XPATH, "//div[contains(@class, '_aatk _aatn')]//video")
#             post_image = video_element.get_attribute("src")  # Store video URL as is
#         except:
#             pass
#     else:
#         try:
#             image_element = driver.find_element(By.XPATH, "//div[contains(@class, '_aagv')]/img")
#             post_image = image_element.get_attribute("src")  # Store image URL (to be uploaded to Cloudinary)
#         except:
#             pass

#     try:
#         caption = driver.find_element(By.XPATH, "//h1[contains(@class, '_ap3a')]").text
#     except:
#         pass

#     driver.quit()
#     return {
#         "url": latest_candidate["url"],
#         "timestamp": latest_candidate["timestamp"],
#         "post_image": post_image,  # Single column for both image & video URL
#         "caption": caption
#     }

# # --- Upload Image to Cloudinary ---
# def upload_to_cloudinary(image_url, page_name):
#     if not image_url or ".mp4" in image_url:  # Skip videos
#         return image_url  # Return as is for videos
#     response = requests.get(image_url)
#     if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
#         cloud_response = cloudinary.uploader.upload(response.content, folder="instagram_post", public_id=page_name)
#         return cloud_response["secure_url"]
#     return None

# # --- Scrape & Store Data in PostgreSQL ---
# def scrape_instagram():
#     conn = psycopg2.connect(DATABASE_URL)
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS instagram_post (
#             id SERIAL PRIMARY KEY,
#             page_name TEXT NOT NULL,
#             link TEXT NOT NULL UNIQUE,
#             post_image TEXT,
#             caption TEXT,
#             timestamp TIMESTAMP
#         );
#     """)
#     conn.commit()

#     for page_name, page_url in INSTAGRAM_PAGES.items():
#         print(f"🔍 Scraping Instagram page: {page_name}")
#         post = get_latest_instagram_post(page_url)
#         if post:
#             final_image_url = upload_to_cloudinary(post["post_image"], page_name)  # Upload images, keep video as is
#             cursor.execute("""
#                 INSERT INTO instagram_post (page_name, link, post_image, caption, timestamp)
#                 VALUES (%s, %s, %s, %s, %s)
#                 ON CONFLICT (link) 
#                 DO UPDATE SET post_image = EXCLUDED.post_image, caption = EXCLUDED.caption, timestamp = EXCLUDED.timestamp
#             """, (page_name, post["url"], final_image_url, post["caption"] or "No caption", post["timestamp"]))
#             conn.commit()
#     cursor.close()
#     conn.close()
#     print("✅ Instagram scraping complete!")

# while True:
#     scrape_instagram()
#     time.sleep(60*20)

































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

# --- PostgreSQL Database ---
DATABASE_URL = "postgresql://instaxrss_user:QGBb5ALqiBraZtjt1c1zoifa4Kf4G1Tu@dpg-cv7sqcqj1k6c739htp00-a.oregon-postgres.render.com/instaxrss"

# --- Cloudinary Configuration ---
cloudinary.config(
    cloud_name="dka67k5av",
    api_key="696938932641642",
    api_secret="Ow7AilWBHGJnkotnC_YVR6xVa6M"
)

# --- Selenium WebDriver Setup ---
insta_options = Options()
insta_options.add_argument("--headless=new")
insta_options.add_argument("--disable-gpu")
insta_options.add_argument("--window-size=375,812")
insta_options.add_argument("--disable-blink-features=AutomationControlled")
insta_options.add_argument(
    "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Mobile Safari/537.36"
)

# --- Instagram Pages ---
INSTAGRAM_PAGES = {
    "Kim Kardashian": "https://www.instagram.com/kimkardashian/",
    "Kylie Jenner": "https://www.instagram.com/kyliejenner/",
    "Rihanna": "https://www.instagram.com/badgalriri/",
    "Kanye West": "https://www.instagram.com/ye/",
    "Justin Bieber": "https://www.instagram.com/justinbieber/",
    "Hailey Bieber": "https://www.instagram.com/haileybieber/",
    "Selena Gomez": "https://www.instagram.com/selenagomez/",
    "Henry Cavill": "https://www.instagram.com/HenryCavill/",
    "Emma Roberts": "https://www.instagram.com/emmaroberts/",
    "Reese Witherspoon": "https://www.instagram.com/reesewitherspoon/",
    "Shakira": "https://www.instagram.com/shakira/",
    "Beyoncé": "https://www.instagram.com/beyonce/",
    "Lady Gaga": "https://www.instagram.com/ladygaga/",
    "Ariana Grande": "https://www.instagram.com/arianagrande/",
    "Billie Eilish": "https://www.instagram.com/billieeilish/",
    "Miley Cyrus": "https://www.instagram.com/mileycyrus/",
    # "Taylor Swift": "https://www.instagram.com/taylorswift/",
    "Gigi Hadid": "https://www.instagram.com/gigihadid/",
    "Zayn Malik": "https://www.instagram.com/zayn/",
    "Tom Cruise": "https://www.instagram.com/tomcruise/",
    "Barry Keoghan": "https://www.instagram.com/barrykeoghansource/",
    "Meghan Markle": "https://www.instagram.com/meghan/",
    "Kendall Jenner": "https://www.instagram.com/kendalljenner/",
    "Kris Jenner": "https://www.instagram.com/krisjenner/",
    "Khloé Kardashian": "https://www.instagram.com/khloekardashian/",
    "Kourtney Kardashian": "https://www.instagram.com/kourtneykardash/",
    "Jeremy Renner": "https://www.instagram.com/jeremyrenner/?hl=en",
    "Chris Hemsworth": "https://www.instagram.com/chrishemsworth/",
    "Ed Sheeran": "https://www.instagram.com/teddysphotos/",
    "Sydney Sweeney": "https://www.instagram.com/sydney_sweeney/",
    "Anne Hathaway": "https://www.instagram.com/annehathaway/",
    "Jennifer Lopez": "https://www.instagram.com/jlo/",
    "Jennifer Garner": "https://www.instagram.com/jennifer.garner/",
    "Jennifer Aniston": "https://www.instagram.com/jenniferaniston/",
    "Jennifer Lawrence": "https://www.instagram.com/1jnnf/",
    # "Meghan Markle": "https://www.instagram.com/meghan/",
    "The Royal Family": "https://www.instagram.com/theroyalfamily/",
    "Cardi B": "https://www.instagram.com/iamcardib/",
    "Soompi": "https://www.instagram.com/soompi/",
    "Katy Perry": "https://www.instagram.com/katyperry/",
    "Paris Hilton": "https://www.instagram.com/parishilton/",
    "Zendaya": "https://www.instagram.com/zendaya/",
    "Jenna Ortega": "https://www.instagram.com/jennaortega/",
    "Netflix": "https://www.instagram.com/netflix/",
    "Tom Hanks": "https://www.instagram.com/tomhanks/",
    "Vin Diesel": "https://www.instagram.com/vindiesel/",
    "Robert Downey Jr.": "https://www.instagram.com/robertdowneyjr/",
    "Prince and Princess of Wales": "https://www.instagram.com/princeandprincessofwales",
    "The Royal Family": "https://www.instagram.com/theroyalfamily",
    "Sarah Ferguson": "https://www.instagram.com/sarahferguson15",
    "Meghan": "https://www.instagram.com/meghan",
    "Duke and Duchess of Sussex Daily": "https://www.instagram.com/dukeandduchessofsussexdaily",
    "Rebecca English": "https://www.instagram.com/byrebeccaenglish",
    "Taylor Swift": "https://www.instagram.com/taylorswift",
    # "Selena Gomez": "https://www.instagram.com/selenagomez",
    "Killatrav": "https://www.instagram.com/killatrav",
    "Princess Eugenie": "https://www.instagram.com/princesseugenie",
    "Ryan Reynolds": "https://www.instagram.com/vancityreynolds",
    # "Kylie Jenner": "https://www.instagram.com/kyliejenner",
    # "Kendall Jenner": "https://www.instagram.com/kendalljenner",
    # "Kim Kardashian": "https://www.instagram.com/kimkardashian",
    "Gigi Hadid": "https://www.instagram.com/gigihadid"
}

# --- Load Instagram Cookies ---
def load_cookies(driver, file_path):
    try:
        cookies = pickle.load(open(file_path, "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        print(f"✅ Cookies loaded from {file_path}!")
    except Exception as e:
        print(f"⚠️ Error loading cookies from {file_path}: {e}")

# --- Extract Latest Post Data ---
def get_latest_instagram_post(page_url):
    driver = webdriver.Chrome(options=insta_options)
    driver.get("https://www.instagram.com/")
    time.sleep(5)
    load_cookies(driver, "instagram_cookies.pkl")
    driver.refresh()
    time.sleep(5)
    driver.get(page_url)
    time.sleep(10)

    # Collect up to 4 candidate post URLs
    candidate_urls = []
    for link in driver.find_elements(By.TAG_NAME, "a"):
        url = link.get_attribute("href")
        if url and ("/p/" in url or "/reel/" in url):
            candidate_urls.append(url)
            if len(candidate_urls) == 4:
                break

    valid_candidates = []
    # For each candidate, check if it's pinned and get its timestamp
    for url in candidate_urls:
        driver.get(url)
        time.sleep(5)

        if driver.find_elements(By.XPATH, "//*[contains(text(), 'Pinned')]"):
            print(f"🔖 Skipping pinned post: {url}")
            continue

        timestamp = None
        try:
            ts_str = driver.find_element(By.TAG_NAME, "time").get_attribute("datetime")
            timestamp = datetime.fromisoformat(ts_str.replace("Z", "+00:00")) if ts_str else None
        except Exception as e:
            print(f"Error getting timestamp for {url}: {e}")

        if timestamp:
            valid_candidates.append({"url": url, "timestamp": timestamp})

    if not valid_candidates:
        driver.quit()
        print("❌ No valid (non-pinned) post found.")
        return None

    # Select the candidate with the latest timestamp
    latest_candidate = max(valid_candidates, key=lambda c: c["timestamp"])
    driver.get(latest_candidate["url"])
    time.sleep(5)

    post_image = None  # Store image or video URL
    caption = ""

    if '/reel/' in latest_candidate["url"]:
        try:
            video_element = driver.find_element(By.XPATH, "//div[contains(@class, '_aatk _aatn')]//video")
            post_image = video_element.get_attribute("src")
        except Exception as e:
            print(f"Error getting video URL: {e}")
    else:
        try:
            image_element = driver.find_element(By.XPATH, "//div[contains(@class, '_aagv')]/img")
            post_image = image_element.get_attribute("src")
        except Exception as e:
            print(f"Error getting image URL: {e}")

    try:
        caption = driver.find_element(By.XPATH, "//h1[contains(@class, '_ap3a')]").text
    except Exception as e:
        print(f"Error getting caption: {e}")

    driver.quit()
    return {
        "url": latest_candidate["url"],
        "timestamp": latest_candidate["timestamp"],
        "post_image": post_image,
        "caption": caption
    }

# --- Upload Image to Cloudinary ---
def upload_to_cloudinary(image_url, page_name):
    if not image_url or ".mp4" in image_url:  # Skip videos
        return image_url  # Return as is for videos
    response = requests.get(image_url)
    if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
        cloud_response = cloudinary.uploader.upload(response.content, folder="instagram_post", public_id=page_name)
        return cloud_response["secure_url"]
    return None

# --- Scrape & Store Data in PostgreSQL ---
def scrape_instagram():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS instagram_post (
            id SERIAL PRIMARY KEY,
            page_name TEXT NOT NULL,
            link TEXT NOT NULL UNIQUE,
            post_image TEXT,
            caption TEXT,
            timestamp TIMESTAMP
        );
    """)
    conn.commit()

    for page_name, page_url in INSTAGRAM_PAGES.items():
        print(f"🔍 Scraping Instagram page: {page_name}")
        post = get_latest_instagram_post(page_url)
        if post:
            final_image_url = upload_to_cloudinary(post["post_image"], page_name)
            cursor.execute("""
                INSERT INTO instagram_post (page_name, link, post_image, caption, timestamp)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (link) 
                DO UPDATE SET post_image = EXCLUDED.post_image, caption = EXCLUDED.caption, timestamp = EXCLUDED.timestamp
            """, (page_name, post["url"], final_image_url, post["caption"] or "No caption", post["timestamp"]))
            conn.commit()
    cursor.close()
    conn.close()
    print("✅ Instagram scraping complete!")

while True:
    scrape_instagram()
    time.sleep(60 * 20)
