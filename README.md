# 🛠️ Shopify API Changelog Notifier

This GitHub Action automatically monitors the [Shopify API Changelog](https://shopify.dev/changelog/feed) and sends you an email whenever a new entry is published. It keeps track of previously read entries using a local JSON file.

## 📦 Features

- Parses Shopify's official changelog RSS feed
- Detects new, unread changelog entries
- Sends a summary email of new entries
- Uses a JSON file (`.changelog_db.json`) to persist state between runs
- Can be scheduled daily or triggered manually

---

## 🚀 Getting Started
### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### 1. Clone this repository

```bash
git clone https://github.com/your-username/shopify-changelog-notifier.git
cd web-scraper-project
```

### 2. Create a virtual environment:
   ```
   python3 -m venv venv
   ```

### 3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

### 4. Install the required packages:
   ```
   pip3 install -r requirements.txt
   ```
