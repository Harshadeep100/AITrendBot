# AITrendBot
AI TrendBot – AI-Powered News Summarizer 🚀

📌 Project Overview
AI TrendBot is an automated AI-powered news summarizer that fetches the latest AI advancements, research, and technology updates, summarizes them using local LLMs (Qwen2.5-3B via Ollama), and sends structured summaries to Discord.

This bot runs twice a day to keep you updated with the most recent AI breakthroughs, ensuring you never miss out on cutting-edge AI developments.

🔹 Features
✅ Fetches only today’s AI news articles (not entire websites)
✅ Uses web scraping (newspaper3k, trafilatura) to extract full articles
✅ Summarizes AI advancements using Qwen2.5-3B (via Ollama)
✅ Sends structured news summaries to Discord
✅ Runs automatically at regular intervals (twice a day)

🛠️ Tech Stack
Python 🐍 – Core scripting
Serper API 🔍 – Fetching AI-related news articles
Ollama (Qwen2.5-3B), OPEN AI API (GPT-4.0), Llama 3.1, Mistral 7B 🧠 – AI-powered summarization
Newspaper3k & Trafilatura 📰 – Extracting full article text
Requests & BeautifulSoup 🌐 – Web scraping & handling news sources
Discord Webhooks 📩 – Sending news summaries to a Discord channel
Used both Task Scheduler and Python schedule ⏳ – Automating execution

📥 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/Harshadeep100/AITrendBot.git
cd AI-TrendBot
2️⃣ Install Dependencies
pip install -r requirements.txt
(Ensure requirements.txt includes: requests, newspaper3k, trafilatura, beautifulsoup4, ollama, schedule.)

3️⃣ Set Up API Keys & Configurations
Get a Serper API Key from Serper.dev.
Set up Ollama and install Qwen2.5-3B:
ollama pull qwen2.5:3b
Create a Discord Webhook and add it to config.py.
4️⃣ Run the Bot
python ai_trendbot.py

🔹 Task Scheduler (Windows)
Open Task Scheduler → Create Basic Task
Set Trigger → Daily (Repeat every 12 hours)
Set Action → Start a Program → Select python.exe
Add Arguments: "C:\path\to\ai_trendbot.py"

📌 Future Improvements
🚀 Convert the bot into an AI Agent for interactive Q&A
🚀 Add voice alerts via AI-generated summaries
🚀 Enable real-time user queries on AI news via a chatbot

🌟 Contribute
Feel free to fork, improve, and submit pull requests! If you encounter issues, open a GitHub issue or reach out.

🚀 AI TrendBot – Stay Ahead in AI Technology! 🤖📡
"Never Miss an AI Breakthrough Again!"
