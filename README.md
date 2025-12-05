# WhatsApp Bot - Twilio Integration

## 📱 Project Overview

WhatsApp Bot is a Python-based application that allows you to send WhatsApp messages using the **Twilio API**. The bot supports both immediate message delivery and scheduled message sending for future dates and times.

Available in two versions:
- **Web Dashboard** (Modern UI) - Recommended ⭐
- **CLI Interface** (Terminal) - Simple & Quick

## ✨ Features

- ✅ Send WhatsApp messages instantly
- ✅ Schedule messages for future delivery
- ✅ Beautiful web dashboard interface
- ✅ User-friendly command-line interface
- ✅ Secure credential management with environment variables
- ✅ Error handling for failed messages
- ✅ Support for multiple recipients
- ✅ Real-time feedback and notifications

## 🔒 Security

Sensitive credentials are stored in `.env` file and excluded from version control via `.gitignore`.

## 🔄 Project Status

⚠️ **IN PROGRESS** - This project is currently under active development with more improvements and features planned:

- 🔜 Database support for message history
- 🔜 Batch message sending
- 🔜 Message templates
- 🔜 Web UI dashboard
- 🔜 Webhook support for incoming messages
- 🔜 Advanced scheduling options (recurring messages)
- 🔜 Message delivery status tracking
- 🔜 Multi-user support

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- Twilio account with WhatsApp sandbox enabled
- pip (Python package manager)

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd WhatsappBot
```

2. Create a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
Create a `.env` file in the project root:
```
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
```

### Usage

Run the application:
```bash
python main.py
```

Follow the prompts to:
- Enter recipient name
- Enter WhatsApp number (with country code)
- Enter message content
- Choose to send now or schedule for later

## 📋 Requirements

- `twilio` - Twilio SDK
- `python-dotenv` - Environment variable management
 `flask` - Web framework for dashboard

## 🐛 Known Issues

- None currently documented

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

Created by Debashish Kashyap

## 📞 Support

For issues or questions, please open an issue in the repository.

---

**Last Updated:** December 5, 2025

