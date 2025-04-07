

import psycopg2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re

# ---------- PostgreSQL Connection ----------
db_url = "postgresql://instaxrss_user:QGBb5ALqiBraZtjt1c1zoifa4Kf4G1Tu@dpg-cv7sqcqj1k6c739htp00-a.oregon-postgres.render.com/instaxrss"

conn = psycopg2.connect(db_url)
cursor = conn.cursor()

# ---------- Create new table ----------
cursor.execute("""
CREATE TABLE IF NOT EXISTS tiktok_link (
    id SERIAL PRIMARY KEY,
    page_name TEXT,
    video_link TEXT UNIQUE,
    img_src TEXT,
    timestamp TEXT,
    date_added TIMESTAMP DEFAULT NOW()
)
""")
conn.commit()

# ---------- Setup Selenium ----------
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
    """
})

# ---------- Fetch old data ----------
cursor.execute("SELECT page_name, video_link, img_src FROM tiktok_links LIMIT 5")
rows = cursor.fetchall()

# Regex to extract only hours, minutes, or days
timestamp_regex = r"(\d+)([hm])|(\d+)d"  # Matches h, m, d units (hours, minutes, days)

# ---------- Process each post ----------
for row in rows:
    page_name, video_link, img_src = row
    print(f"Processing: {video_link}")

    try:
        driver.get(video_link)
        time.sleep(15)  # wait for page to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        anchor = soup.find('a', {'class': 'css-qvpt8d-StyledAuthorAnchor'})  # change if needed
        date = None
        if anchor:
            strings = list(anchor.stripped_strings)
            if strings:
                date = strings[-1]

        # Extract timestamp using regex
        if date:
            match = re.search(timestamp_regex, date)  # Match hours, minutes, or days
            if match:
                timestamp = match.group(0)  # Get the matched time string
                print(f"Valid Timestamp: {timestamp}")
            else:
                print("❌ Invalid Timestamp")
                continue
        else:
            print("❌ No Timestamp Found")
            continue

        # Insert into new table
        cursor.execute("""
            INSERT INTO tiktok_link (page_name, video_link, img_src, post_time)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (page_name, video_link, img_src, timestamp))
        conn.commit()
        print("✅ Inserted Successfully\n")

    except Exception as e:
        print("❌ Error processing:", video_link)
        print(e)
        continue

# ---------- Cleanup ----------
driver.quit()
cursor.close()
conn.close()

print("✅ All Done")
