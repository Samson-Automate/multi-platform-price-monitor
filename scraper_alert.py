import json
import os
import sqlite3
import time
import logging
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import schedule

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

DB_NAME = "price_history.db"

def init_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            url TEXT,
            price REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()
    logging.info("Database initialized successfully.")

def get_last_price(product_url):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT price FROM prices WHERE url = ? ORDER BY id DESC LIMIT 1", (product_url,))
    row = cursor.fetchone()
    conn.close()
    return row if row else None

def save_new_price(product_name, url, price):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO prices (product_name, url, price, timestamp) VALUES (?, ?, ?, ?)",
        (product_name, url, price, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

def send_discord_alert(webhook_url, message):
    payload = {"content": message}
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code in [200, 204]:
            logging.info("Discord notification sent successfully.")
        else:
            logging.error(f"Discord failed: {response.text}")
    except Exception as e:
        logging.error(f"Error sending Discord alert: {e}")

def scrape_ebay_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, "html.parser")
        price_span = soup.find("span", {"class": "ux-textspans"}) or soup.find("div", {"class": "x-price-primary"})
        if price_span:
            price_text = price_span.text.strip()
            clean_price = "".join(c for c in price_text if c.isdigit() or c == '.')
            return float(clean_price)
        return None
    except Exception as e:
        logging.error(f"Scraping error for {url}: {e}")
        return None

def monitor_job():
    logging.info("Starting automation check cycle...")
    if not os.path.exists("config.json"):
        logging.error("config.json file missing!")
        return
    with open("config.json", "r") as f:
        config = json.load(f)

    webhook_url = config.get("discord_webhook_url")
    products = config.get("products_to_track", [])

    for product in products:
        name = product["name"]
        url = product["url"]

        logging.info(f"Checking product: {name}")
        current_price = scrape_ebay_price(url)

        if current_price is None:
            continue

        last_price = get_last_price(url)

        if last_price is None:
            logging.info(f"First log for {name}. Price: ${current_price}")
            save_new_price(name, url, current_price)
        elif current_price < last_price:
            msg = f"🚨 **PRICE DROP ALERT!** 🚨\n\n📦 **Product:** {name}\n📉 **Old Price:** ${last_price}\n🔥 **New Price:** ${current_price}\n🔗 **Link:** {url}"
            send_discord_alert(webhook_url, msg)
            save_new_price(name, url, current_price)
        elif current_price > last_price:
            logging.info(f"{name} price increased from ${last_price} to ${current_price}. Updating DB.")
            save_new_price(name, url, current_price)
        else:
            logging.info(f"No price change for {name} (${current_price}).")

    logging.info("Cycle complete. Waiting for next schedule.")

if __name__ == "__main__":
    init_database()
    monitor_job()
    with open("config.json", "r") as f:
        config = json.load(f)
    interval = config.get("check_interval_minutes", 60)
    schedule.every(interval).minutes.do(monitor_job)

    logging.info(f"Automation schedule set for every {interval} minutes. Script is running active...")
    while True:
        schedule.run_pending()
        time.sleep(1)
