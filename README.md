# 🛠️ Shopify API Changelog Notifier

This GitHub Action automatically monitors the [Shopify API Changelog](https://shopify.dev/changelog/feed) and sends you an email whenever a new entry is published. It keeps track of previously read entries using a persistent database to avoid duplicate notifications.

## 📦 Features

- ✅ Parses Shopify's official changelog RSS feed
- ✅ Detects new, unread changelog entries  
- ✅ Sends beautifully formatted HTML email summaries
- ✅ Persists state between runs (no duplicate notifications)
- ✅ Supports multiple email recipients
- ✅ Configurable SMTP settings
- ✅ Can be scheduled daily or triggered manually
- ✅ Robust error handling and logging

---

## 🚀 Quick Setup (GitHub Actions)

### 1. Fork or Clone this Repository

```bash
git clone https://github.com/RatulHasan/shopify-changelog-notifier.git
cd shopify-changelog-notifier
```

### 2. Set up GitHub Secrets

Go to your repository → **Settings** → **Secrets and variables** → **Actions** and add these secrets:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `TO_EMAIL` | Recipient email(s) (comma-separated) | `john@example.com,team@company.com` |
| `FROM_EMAIL` | Sender email address | `notifications@yourdomain.com` |
| `SMTP_USER` | SMTP username (usually same as FROM_EMAIL) | `notifications@yourdomain.com` |
| `SMTP_PASS` | SMTP password or app password | `your-app-password` |
| `SMTP_SERVER` | SMTP server hostname | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port number | `587` |

### 3. Enable GitHub Actions

The workflow will automatically run daily at 11 AM UTC+6 (5 AM UTC). You can also trigger it manually from the **Actions** tab.

### 4. Configure Repository Permissions

Ensure your repository has write permissions:
- Go to **Settings** → **Actions** → **General**
- Under "Workflow permissions", select **"Read and write permissions"**

---

## 📧 Email Provider Setup

### Gmail Setup
1. Enable 2-factor authentication on your Google account
2. Generate an App Password: [Google Account Settings](https://myaccount.google.com/apppasswords)
3. Use your App Password as `SMTP_PASS`

### Other Email Providers
| Provider | SMTP Server | Port |
|----------|-------------|------|
| **Outlook/Hotmail** | `smtp.live.com` | `587` |
| **Yahoo** | `smtp.mail.yahoo.com` | `587` |
| **Custom SMTP** | Your server | Usually `587` or `465` |

---

## 🧪 Local Development

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/shopify-changelog-notifier.git
   cd shopify-changelog-notifier
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install feedparser
   ```

5. **Set environment variables:**
   ```bash
   # Create a .env file or export directly:
   export TO_EMAIL="your-email@example.com"
   export FROM_EMAIL="sender@example.com"
   export SMTP_USER="sender@example.com"
   export SMTP_PASS="your-app-password"
   export SMTP_SERVER="smtp.gmail.com"
   export SMTP_PORT="587"
   ```

6. **Run the script:**
   ```bash
   python scripts/fetch_changelog.py
   ```

---

## 📁 Project Structure

```
shopify-changelog-notifier/
├── .github/
│   └── workflows/
│       └── changelog-notifier.yml    # GitHub Actions workflow
├── scripts/
│   └── fetch_changelog.py           # Main Python script
├── .changelog_db.json               # Database file (auto-generated)
├── .gitignore
└── README.md
```

---

## ⚙️ Configuration Options

### Scheduling
Modify the cron schedule in `.github/workflows/changelog-notifier.yml`:
```yaml
schedule:
  - cron: '0 5 * * *'  # Daily at 5 AM UTC (11 AM UTC+6)
```

### Email Template
Customize the HTML email template in `scripts/fetch_changelog.py` around line 65.

### Database Format
The script supports both JSON and text file formats for the database. See the script for implementation details.

---

## 🔧 Troubleshooting

### Common Issues

**❌ "Authentication failed"**
- Verify your SMTP credentials
- For Gmail, ensure you're using an App Password, not your regular password
- Check if 2FA is enabled (required for Gmail App Passwords)

**❌ "No new changelog entries" (but you expect some)**
- Check if `.changelog_db.json` exists and contains previous entries
- Manually delete the database file to reset and get all current entries

**❌ "Failed to fetch RSS feed"**
- Verify internet connectivity
- Check if Shopify's changelog feed is accessible: https://shopify.dev/changelog/feed

**❌ GitHub Actions permission denied**
- Ensure repository has "Read and write permissions" enabled
- Check that the workflow has `permissions: contents: write`

### Debug Mode
Add debug logging by modifying the script to include more verbose output.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Shopify Developer Changelog](https://shopify.dev/changelog/) for providing the RSS feed
- [feedparser](https://pypi.org/project/feedparser/) for RSS parsing capabilities