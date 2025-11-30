# 🤖 Telegram AI Chatbot

Advanced Telegram chatbot powered by GitHub Models API with custom system prompts, multiple AI models, and conversation management.

## ✨ Features

### Core Features
- 🧠 **Multiple AI Models**: GPT-4o, GPT-4o Mini, Llama 3.1, Mistral, Phi-3
- 📝 **Custom System Prompts**: Personalize AI behavior for your needs
- 🌡️ **Temperature Control**: Adjust creativity from focused to creative
- 💬 **Conversation History**: Maintains context across messages
- 📊 **Usage Statistics**: Track your interactions
- 📤 **Export Conversations**: Download chat history as text

### Advanced Features
- ⚙️ **Settings Management**: View and modify all settings
- 🔄 **Conversation Reset**: Clear history anytime
- 🎯 **Model Selection UI**: Easy model switching with inline buttons
- 📈 **Smart Context Management**: Automatic history trimming
- 🛡️ **Error Handling**: Robust error recovery
- 📱 **User-Friendly Commands**: Intuitive command structure

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- GitHub Personal Access Token

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/nihanislam/telegram-ai-chatbot.git
cd telegram-ai-chatbot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your tokens
```

4. **Run the bot**
```bash
python bot.py
```

## 📋 Commands

### Basic Commands
- `/start` - Welcome message and quick start
- `/help` - Full command list and documentation

### Configuration
- `/model` - Select AI model (GPT-4o, Llama, Mistral, etc.)
- `/setprompt <text>` - Set custom system prompt
- `/temperature <0.0-2.0>` - Adjust response creativity
- `/settings` - View current configuration

### Conversation Management
- `/reset` - Clear conversation history
- `/export` - Download conversation as text file
- `/stats` - View usage statistics

## 🎯 Usage Examples

### Setting Custom Prompts
```
/setprompt You are a Python expert who explains code clearly and concisely
```

### Adjusting Temperature
```
/temperature 1.2
```
- **0.0-0.3**: Very focused, deterministic
- **0.4-0.7**: Balanced (default: 0.7)
- **0.8-1.2**: Creative, varied
- **1.3-2.0**: Very creative, unpredictable

## 🤖 Available Models

| Model | Description | Best For |
|-------|-------------|----------|
| 🧠 GPT-4o | Most capable | Complex tasks, reasoning |
| ⚡ GPT-4o Mini | Fast & efficient | Quick responses, general chat |
| 🦙 Llama 3.1 70B | Open source | Balanced performance |
| 🦙 Llama 3.1 405B | Largest open model | Advanced reasoning |
| 🌪️ Mistral Large | Balanced | General purpose |
| 🔬 Phi-3 Medium | Compact | Efficient processing |

## 🏗️ Project Structure

```
telegram-ai-chatbot/
├── bot.py              # Main bot logic
├── config.py           # Configuration & settings
├── models.py           # GitHub API integration
├── user_manager.py     # User data management
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
├── .gitignore         # Git ignore rules
├── Procfile           # Deployment config
├── runtime.txt        # Python version
└── README.md          # Documentation
```

## 🌐 Deployment

### Railway (Recommended)

1. **Create Railway account**: [railway.app](https://railway.app)

2. **Deploy from GitHub**:
   - Connect your GitHub repository
   - Add environment variables:
     - `TELEGRAM_BOT_TOKEN`
     - `GITHUB_TOKEN`
   - Deploy!

3. **Monitor**: Check logs in Railway dashboard

### Heroku

```bash
heroku create your-bot-name
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set GITHUB_TOKEN=your_github_token
git push heroku main
```

### DigitalOcean / VPS

```bash
# SSH into your server
git clone https://github.com/nihanislam/telegram-ai-chatbot.git
cd telegram-ai-chatbot
pip install -r requirements.txt

# Create .env file
nano .env

# Run with screen or tmux
screen -S telegram-bot
python bot.py
# Ctrl+A, D to detach
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather | Yes |
| `GITHUB_TOKEN` | GitHub Personal Access Token | Yes |

### Getting Tokens

**Telegram Bot Token:**
1. Message [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Follow instructions
4. Copy the token

**GitHub Token:**
1. Go to [GitHub Settings → Tokens](https://github.com/settings/tokens)
2. Generate new token (classic)
3. Select scopes: `repo`, `read:org`
4. Copy the token

## 📊 Features Roadmap

### Phase 1 ✅ (Current)
- [x] Multiple AI models
- [x] Custom system prompts
- [x] Temperature control
- [x] Conversation management
- [x] Export functionality
- [x] Usage statistics

### Phase 2 🚧 (In Progress)
- [ ] Database integration (PostgreSQL)
- [ ] User authentication
- [ ] Rate limiting
- [ ] Admin panel
- [ ] Multi-language support

### Phase 3 📅 (Planned)
- [ ] Image generation support
- [ ] Voice message support
- [ ] Group chat support
- [ ] Webhook mode
- [ ] Analytics dashboard
- [ ] Premium features

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Issues

Found a bug? Have a feature request? Please [open an issue](https://github.com/nihanislam/telegram-ai-chatbot/issues).

## 📧 Contact

- GitHub: [@nihanislam](https://github.com/nihanislam)
- Repository: [telegram-ai-chatbot](https://github.com/nihanislam/telegram-ai-chatbot)

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [GitHub Models](https://github.com/marketplace/models) - Free AI model access
- [httpx](https://www.python-httpx.org/) - HTTP client

---

⭐ **Star this repo if you find it useful!**

Made with ❤️ by [nihanislam](https://github.com/nihanislam)