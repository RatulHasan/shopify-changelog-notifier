import os
import json
import feedparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ---------------------------
# 🔧 Configuration
# ---------------------------

FEED_URL = "https://shopify.dev/changelog/feed"
DB_FILE = ".changelog_db.json"


# Load required environment variables
def get_env(name, default=None, required=False):
    value = os.getenv(name, default)
    if required and not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


TO_EMAILS = [email.strip() for email in get_env("TO_EMAIL", required=True).split(",") if email.strip()]
FROM_EMAIL = get_env("FROM_EMAIL", required=True)
SMTP_USER = get_env("SMTP_USER", required=True)
SMTP_PASS = get_env("SMTP_PASS", required=True)
SMTP_SERVER = get_env("SMTP_SERVER", "smtp.gmail.com")

# Fix: Handle SMTP_PORT conversion with proper error handling
smtp_port_str = get_env("SMTP_PORT", "587")
try:
    SMTP_PORT = int(smtp_port_str)
except ValueError:
    print(f"⚠️  Invalid SMTP_PORT value: '{smtp_port_str}'. Using default port 587.")
    SMTP_PORT = 587

# ---------------------------
# 📦 Load previously seen entries
# ---------------------------

if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        seen_links = set(json.load(f))
else:
    seen_links = set()

# ---------------------------
# 📡 Fetch and parse RSS feed
# ---------------------------

try:
    feed = feedparser.parse(FEED_URL)
    if not feed.entries:
        print("⚠️  No entries found in the RSS feed.")
        exit(0)

    new_entries = [entry for entry in feed.entries if entry.link not in seen_links]
except Exception as e:
    print(f"❌ Failed to fetch RSS feed: {e}")
    exit(1)

if not new_entries:
    print("✅ No new changelog entries.")
    exit(0)

print(f"📰 Found {len(new_entries)} new changelog entries.")

# ---------------------------
# 📧 Construct HTML email body
# ---------------------------

html_body = """
<h2>🛠️ Shopify API - New Changelog Entries</h2>
<ul style="font-family: Arial, sans-serif; font-size: 14px;">
"""

for entry in reversed(new_entries):  # oldest first
    # Safely handle missing attributes
    title = getattr(entry, 'title', 'No title')
    link = getattr(entry, 'link', '#')
    published = getattr(entry, 'published', 'No date')
    summary = getattr(entry, 'summary', 'No summary available')

    html_body += f"""
    <li style="margin-bottom: 20px;">
        <strong>{title}</strong><br />
        <a href="{link}">{link}</a><br />
        <em>{published}</em><br />
        <p>{summary}</p>
    </li>
    """

html_body += "</ul>"

# ---------------------------
# 📤 Send email to each recipient
# ---------------------------

email_success_count = 0
for email in TO_EMAILS:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🛠️ New Shopify API Changelog Entries"
    msg["From"] = FROM_EMAIL
    msg["To"] = email

    html_part = MIMEText(html_body, "html")
    msg.attach(html_part)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg, to_addrs=[email])
            print(f"📧 HTML email sent to {email}")
            email_success_count += 1
    except Exception as e:
        print(f"❌ Failed to send email to {email}: {e}")

# ---------------------------
# 💾 Update the seen database (only if emails were sent successfully)
# ---------------------------

if email_success_count > 0:
    seen_links.update(entry.link for entry in new_entries)
    try:
        with open(DB_FILE, "w") as f:
            json.dump(list(seen_links), f)
        print("✅ Updated changelog DB.")
    except Exception as e:
        print(f"❌ Failed to update changelog DB: {e}")
else:
    print("⚠️  No emails sent successfully. Not updating changelog DB.")

print(f"✅ Process completed. {email_success_count}/{len(TO_EMAILS)} emails sent successfully.")