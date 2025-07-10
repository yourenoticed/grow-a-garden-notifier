# Grow a Garden notification bot

## How to start the bot:

### If it's the first time you start a bot

1. Create a file **config.py** in this directory

   - Add **BOT_TOKEN = "YOUR BOT TOKEN"** to the file. You can get the bot token from [BotFather](https://t.me/BotFather)

2. Install Python 3.12
3. Create and activate a virtual environment:

   1. Run **python -m venv .venv** in your terminal
   2. Run **source .venv/Scripts/activate** if you use Bash or **source .venv/Scripts/activate.bat** in the Command Prompt

4. Run **pip install -r requirements.txt** in your terminal

### If you've done all the steps above:

1. Open two terminals and activate virtual environments (step 3.2)
2. Run **python bot.py** in one terminal
3. Run **python notifier.py** in another terminal
