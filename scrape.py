from playwright.sync_api import sync_playwright
from datetime import date
import csv
import os

URL = "https://www.screener.in/screens/3400687/52wk-high-stocks/"
TODAY = date.today().isoformat()
DATA_FILE = "data/industry_data.csv"

os.makedirs("data", exist_ok=True)

def scrape():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120 Safari/537.36"
            )
        )

        page = context.new_page()
        page.goto(URL, wait_until="networkidle", timeout=60000)

        # Open Industry dropdown
        page.wait_for_selector("button:has-text('Industry')")
        page.click("button:has-text('Industry')")
        page.wait_for_timeout(800)

        # Wait for industries to load
        page.wait_for_selector("div[role='menu'] label")

        items = page.locator("div[role='menu'] label").all()

        rows = []
        for item in items:
            text = item.inner_text().strip()
            if "-" in text:
                industry, count = text.rsplit("-", 1)
                rows.append([TODAY, industry.strip(), int(count.strip())])

        bro
