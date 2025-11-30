import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from config import TELEGRAM_TOKEN, AVAILABLE_MODELS
from models import GitHubModelsAPI
from user_manager import UserManager

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize
api = GitHubModelsAPI()
user_manager = UserManager()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    welcome_text = """
🤖 **Welcome to AI Chat Bot!**

I'm powered by GitHub's free AI models with advanced features!

**Quick Start:**
/model - Choose your AI model
/setprompt - Customize my behavior
/settings - View your settings
/help - Full command list

Just send me a message to start chatting! 💬
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command handler"""
    help_text = """
📚 **Available Commands:**

**Basic:**
/start - Welcome message
/help - Show this help

**Configuration:**
/model - Select AI model (GPT-4o, Llama, Mistral, etc.)
/setprompt <text> - Set custom system prompt
/temperature <0.0-2.0> - Adjust creativity (default: 0.7)
/settings - View current settings

**Conversation:**
/reset - Clear conversation history
/export - Export conversation as text
/stats - View usage statistics

**Examples:**
`/setprompt You are a Python coding expert`
`/temperature 1.2`

**Available Models:**
🧠 GPT-4o - Most capable
⚡ GPT-4o Mini - Fast & efficient
🦙 Llama 3.1 (70B/405B) - Open source
🌪️ Mistral Large - Balanced
🔬 Phi-3 Medium - Compact

**Tips:**
• Higher temperature = more creative
• Lower temperature = more focused
• Custom prompts reset conversation
• Max 20 messages kept in history
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def model_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Model selection command"""
    keyboard = []
    for key, model in AVAILABLE_MODELS.items():
        keyboard.append([InlineKeyboardButton(
            f"{model['emoji']} {model['display']}", 
            callback_data=f"model_{key}"
        )])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🤖 **Select AI Model:**\n\nChoose the model that fits your needs:", 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )

async def model_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle model selection"""
    query = update.callback_query
    await query.answer()
    
    model_key = query.data.split('_')[1]
    model_info = AVAILABLE_MODELS[model_key]
    
    user_id = query.from_user.id
    user_manager.set_model(user_id, model_info['name'])
    
    await query.edit_message_text(
        f"✅ Model set to: **{model_info['emoji']} {model_info['display']}**\n\n"
        f"Start chatting to see it in action!",
        parse_mode='Markdown'
    )

async def setprompt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set custom system prompt"""
    if not context.args:
        current_user = user_manager.get_user(update.effective_user.id)
        await update.message.reply_text(
            "📝 **Set Custom System Prompt**\n\n"
            f"**Current prompt:**\n_{current_user['system_prompt']}_\n\n"
            "**Usage:** `/setprompt Your custom instruction here`\n\n"
            "**Examples:**\n"
            "• `/setprompt You are a Python expert who explains code clearly`\n"
            "• `/setprompt You are a creative writer helping with stories`\n"
            "• `/setprompt You are a friendly teacher for kids`",
            parse_mode='Markdown'
        )
        return
    
    prompt = ' '.join(context.args)
    user_id = update.effective_user.id
    user_manager.set_system_prompt(user_id, prompt)
    
    await update.message.reply_text(
        f"✅ **System prompt updated!**\n\n"
        f"New prompt: _{prompt}_\n\n"
        f"⚠️ Conversation history has been reset.",
        parse_mode='Markdown'
    )

async def temperature_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set temperature for responses"""
    if not context.args:
        current_user = user_manager.get_user(update.effective_user.id)
        await update.message.reply_text(
            f"🌡️ **Current temperature:** {current_user['temperature']}\n\n"
            "**Usage:** `/temperature <0.0-2.0>`\n\n"
            "**Guide:**\n"
            "• 0.0-0.3: Very focused, deterministic\n"
            "• 0.4-0.7: Balanced (default: 0.7)\n"
            "• 0.8-1.2: Creative, varied\n"
            "• 1.3-2.0: Very creative, unpredictable\n\n"
            "**Example:** `/temperature 1.0`",
            parse_mode='Markdown'
        )
        return
    
    try:
        temp = float(context.args[0])
        if temp < 0.0 or temp > 2.0:
            raise ValueError()
        
        user_id = update.effective_user.id
        user_manager.set_temperature(user_id, temp)
        
        await update.message.reply_text(
            f"✅ Temperature set to: **{temp}**\n\n"
            f"{'🎯 Focused mode' if temp < 0.5 else '🎨 Creative mode' if temp > 1.0 else '⚖️ Balanced mode'}",
            parse_mode='Markdown'
        )
    except (ValueError, IndexError):
        await update.message.reply_text(
            "❌ Invalid temperature. Please use a number between 0.0 and 2.0\n"
            "Example: `/temperature 0.7`",
            parse_mode='Markdown'
        )

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show current settings"""
    user_id = update.effective_user.id
    user_data = user_manager.get_user(user_id)
    
    model_name = "Unknown"
    for model in AVAILABLE_MODELS.values():
        if model['name'] == user_data['model']:
            model_name = f"{model['emoji']} {model['display']}"
            break
    
    settings_text = f"""
⚙️ **Your Current Settings**

**Model:** {model_name}
**Temperature:** {user_data['temperature']}
**Messages in history:** {len(user_data['conversation'])}

**System Prompt:**
_{user_data['system_prompt']}_

Use /model, /setprompt, or /temperature to change settings.
    """
    await update.message.reply_text(settings_text, parse_mode='Markdown')

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show usage statistics"""
    user_id = update.effective_user.id
    stats = user_manager.get_stats(user_id)
    
    stats_text = f"""
📊 **Your Statistics**

**Total messages sent:** {stats['message_count']}
**Current conversation length:** {stats['conversation_length']} messages
**Active model:** {stats['current_model']}
**Temperature:** {stats['temperature']}

Keep chatting to see your stats grow! 🚀
    """
    await update.message.reply_text(stats_text, parse_mode='Markdown')

async def export_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Export conversation history"""
    user_id = update.effective_user.id
    conversation = user_manager.export_conversation(user_id)
    
    if len(user_manager.get_user(user_id)['conversation']) == 0:
        await update.message.reply_text("📭 No conversation to export yet. Start chatting first!")
        return
    
    # Send as text file
    await update.message.reply_document(
        document=conversation.encode('utf-8'),
        filename=f"conversation_{user_id}.txt",
        caption="📄 Your conversation history"
    )

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reset conversation history"""
    user_id = update.effective_user.id
    user_manager.reset_conversation(user_id)
    await update.message.reply_text(
        "🔄 **Conversation history cleared!**\n\n"
        "Starting fresh. Your settings remain unchanged."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages"""
    user_id = update.effective_user.id
    user_message = update.message.text
    
    # Show typing indicator
    await update.message.chat.send_action("typing")
    
    # Add user message to conversation
    user_manager.add_message(user_id, "user", user_message)
    
    # Get user's model and messages
    user_data = user_manager.get_user(user_id)
    messages = user_manager.get_messages(user_id)
    
    # Call API
    response = await api.chat_completion(
        user_data['model'], 
        messages,
        temperature=user_data['temperature']
    )
    
    if "error" in response:
        await update.message.reply_text(
            f"❌ **Error occurred:**\n{response['error']}\n\n"
            f"Try again or use /model to switch models."
        )
        return
    
    # Extract AI response
    try:
        ai_message = response['choices'][0]['message']['content']
        
        # Add AI response to conversation
        user_manager.add_message(user_id, "assistant", ai_message)
        
        # Send response (split if too long)
        if len(ai_message) > 4096:
            for i in range(0, len(ai_message), 4096):
                await update.message.reply_text(ai_message[i:i+4096])
        else:
            await update.message.reply_text(ai_message)
            
    except (KeyError, IndexError) as e:
        logger.error(f"Error parsing response: {e}")
        await update.message.reply_text(
            "❌ Unexpected response format. Please try again."
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ An error occurred. Please try again or contact support."
        )

def main():
    """Start the bot"""
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found!")
        return
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("model", model_command))
    application.add_handler(CommandHandler("setprompt", setprompt_command))
    application.add_handler(CommandHandler("temperature", temperature_command))
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("export", export_command))
    application.add_handler(CommandHandler("reset", reset_command))
    
    # Callback handlers
    application.add_handler(CallbackQueryHandler(model_callback, pattern="^model_"))
    
    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    logger.info("🤖 Bot started successfully!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()