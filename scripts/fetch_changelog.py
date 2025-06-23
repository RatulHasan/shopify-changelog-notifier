import feedparser
import os
import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# --- Config ---
FEED_URL = "https://shopify.dev/changelog/feed"
DB_FILE = ".changelog_db.json"
TO_EMAIL = os.getenv("TO_EMAIL")
FROM_EMAIL = os.getenv("FROM_EMAIL")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

# --- Load database ---
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        seen_links = set(json.load(f))
else:
    seen_links = set()

# --- Parse RSS feed ---
feed = feedparser.parse(FEED_URL)
new_entries = []

for entry in feed.entries:
    if entry.link not in seen_links:
        new_entries.append(entry)

# Get list of recipients from TO_EMAIL (comma-separated)
TO_EMAILS = [email.strip() for email in os.getenv("TO_EMAIL", "").split(",") if email.strip()]

if new_entries and TO_EMAILS:
    new_entries.reverse()
    msg_body = "\n\n".join([
        f"🆕 {e.title}\n{e.link}\n{e.published}\n\n{e.summary}"
        for e in new_entries
    ])

    # Loop through each email and send individually
    for email in TO_EMAILS:
        msg = MIMEText(msg_body, "plain")
        msg["Subject"] = "🛠️ New Shopify API Changelog Entries"
        msg["From"] = FROM_EMAIL
        msg["To"] = email

        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg, to_addrs=[email])
            server.quit()
            print(f"📧 Email sent to {email}")
        except Exception as e:
            print(f"❌ Failed to send email to {email}: {e}")

    # --- Update DB ---
    seen_links.update(e.link for e in new_entries)
    with open(DB_FILE, "w") as f:
        json.dump(list(seen_links), f)
else:
    print("✅ No new changelog entries.")
