import requests
import openai
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackContext, ContextTypes, ApplicationBuilder, MessageHandler, filters
from redis_utils import reset_daily_limits, redis_client
from scheduler import start_scheduler
from config import TELEGRAM_BOT_TOKEN, CLIENT_ID, REDIRECT_URI, CLIENT_SECRET, GITHUB_URL_API
from config import logger

application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! This is your GitHub bot.")

start_handler = CommandHandler("start", start)
application.add_handler(start_handler)

async def auth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send the GitHub OAuth authorization URL to the user."""
    auth_url = (
        f"https://github.com/login/oauth/authorize?"
        f"client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=repo"
    )
    await update.message.reply_text(f"Please authorize the bot to access your GitHub account: {auth_url}")

async def github_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the callback from GitHub and exchange the authorization code for an access token."""
    query = update.message.text
    code = query.split("code=")[-1]  # Extract the code from the message

    # Exchange the code for an access token
    token_url = "https://github.com/login/oauth/access_token"
    token_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    headers = {'Accept': 'application/json'}
    response = requests.post(token_url, data=token_data, headers=headers)

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        chat_id = update.message.chat_id
        # Store access token in Redis, tied to the chat ID
        redis_client.set(f"github_access_token_{chat_id}", access_token)
        await update.message.reply_text("GitHub account successfully authorized.")
    else:
        await update.message.reply_text(f"Authorization failed: {response.status_code}")

async def github_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetch and display a summary of the user's GitHub repositories."""
    username = context.user_data["username"]
    try:
        response = requests.get(f'{GITHUB_URL_API}/users/{username}/repos')
        if response.status_code == 200:
            repos = response.json()
            total_repos = len(repos)
            languages = set([repo['language'] for repo in repos if repo['language']])

            msg = f"GitHub stats for {username}:\n\n"
            msg += f"Total Repositories: {total_repos}\n"
            msg += f"Languages Used: {', '.join(languages)}\n"

            await update.message.reply_text(msg)
        else:
            await update.message.reply_text(f"Error fetching GitHub stats: {response.status_code}")
    except Exception as e:
        logger.error(f"Error fetching GitHub stats: {e}")
        await update.message.reply_text("Failed to fetch GitHub stats.")


async def request_to_join_chat(update: Update, context: CallbackContext):
    """Handles user requests to join a specific Telegram chat."""
    await update.message.reply_text("To join the chat, send your GitHub username and request reason.")

async def handle_join_request(update: Update, context: CallbackContext):
    """Process the user's join request."""
    chat_id = update.message.chat_id
    user_input = update.message.text
    await update.message.reply_text(f"Request received. We will review it shortly!\nYour request: {user_input}")


async def ai_code_help(update: Update, context: CallbackContext):
    """Provide AI-powered code suggestions"""
    user_query = update.message.text
    
    try:
        # Calling OpenAI's Completion API to generate code
        response = openai.completions.create(
            engine="davinci-codex", 
            prompt=f"Write a Python function to {user_query}",
            max_tokens=150,
            temperature=0.5
        )
        
        code_snippet = response.choices[0].text.strip()
    except Exception as e:
        code_snippet = f"Failed to generate code due to: {str(e)}"

    # Formatting the output to send to the user
    gpt_output = f"Based on your query '{user_query}', here's a Python code snippet:\n```python\n{code_snippet}\n```"
    await update.message.reply_text(gpt_output, parse_mode=ParseMode.MARKDOWN)

def main():
    """Start the bot."""
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("github", auth))
    application.add_handler(CommandHandler("stats", github_stats))
    application.add_handler(CommandHandler("joinchat", request_to_join_chat))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_join_request))
    application.add_handler(CommandHandler("codehelp", ai_code_help))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    # Start Scheduler and Bot Polling
    start_scheduler()
    main()
