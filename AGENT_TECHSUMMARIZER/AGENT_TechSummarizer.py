import requests
import openai
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import trafilatura
from newspaper import Article
from bs4 import BeautifulSoup
import requests


# Configuration (Update these before running)
SERPER_API_KEY = "your_serper_API_key"
HUGGINGFACE_API_KEY = "your_huggingfacehub_api_key"
EMAIL_SENDER = "your email"
EMAIL_PASSWORD = " "  # enable "App Passwords"
EMAIL_RECEIVER = "your email"
DISCORD_WEBHOOK_URL = "you discord server webhook"


# Function to fetch AI news using Serper API
def fetch_ai_news():
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}

    # Improve search query to target AI advancements and filter by today’s news
    payload = json.dumps({
        "q": "latest AI technology news today OR AI breakthroughs today OR new AI research published today OR AI model release today OR AI innovation announced today",
        "gl": "us",
        "hl": "en",
        "num": 5,  # Limit to only 5 articles for better quality
        "tbs": "qdr:d"  # Google filter to get results only from the last 24 hours
    })

    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        results = response.json()
        return results.get("organic", [])  # Extracts search results
    else:
        print("Failed to fetch news:", response.text)
        return []


def extract_article_text(url):
    try:
        # First try newspaper3k (works well on structured news pages)
        article = Article(url)
        article.download()
        article.parse()
        return article.text.strip()  # Returns clean article text
    except:
        print(f"Newspaper3k failed for {url}. Trying trafilatura...")

    # Try trafilatura as a fallback (works better for modern sites)
    try:
        downloaded = trafilatura.fetch_url(url)
        extracted_text = trafilatura.extract(downloaded, include_links=False, include_comments=False)

        if extracted_text and len(extracted_text) > 500:  # Ensure valid content
            return extracted_text
        else:
            print(f"Skipping {url} (No useful content)")
            return None
    except Exception as e:
        print(f"Error extracting article from {url}: {str(e)}")
        return None

# Function to summarize articles using OpenAI

import ollama

def summarize_text(text):
    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "user",
                "content": f"Summarize this AI news article in a structured format. Extract key innovations, technical advancements, and industry impact:\n\n{text}"
            }
        ]
    )
    return response["message"]["content"]

# Function to send email
def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", str(e))

# Function to send summary to Discord
def send_to_discord(summary):
    max_length = 1900  # Discord limit is 2000, keep some buffer
    messages = [summary[i:i + max_length] for i in range(0, len(summary), max_length)]

    for message in messages:
        data = {"content": message}
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)

        if response.status_code == 204:
            print("Message posted to Discord successfully!")
        else:
            print("Failed to post to Discord:", response.text)


def fetch_and_summarize_news():
    news_articles = fetch_ai_news()
    summaries = []

    for article in news_articles:
        title = article.get("title", "No Title")
        link = article.get("link", "#")

        # Extract full news/article text
        full_text = extract_article_text(link)
        if not full_text:
            continue  # Skip if extraction fails

        summary = summarize_text(full_text)
        summaries.append(f"**{title}**\n{summary}\n[Read more]({link})\n")

    return "\n\n".join(summaries)

# Main Execution
if __name__ == "__main__":
    print("Fetching AI news...")
    news_articles = fetch_ai_news()

    if not news_articles:
        print("No news found.")
        exit()

    summaries = []
    for article in news_articles:
        title = article.get("title", "No Title")
        link = article.get("link", "#")
        snippet = article.get("snippet", "No description available.")

        full_text = f"Title: {title}\nDescription: {snippet}\nLink: {link}"
        summary = summarize_text(full_text)

        summaries.append(f"**{title}**\n{summary}\n[Read more]({link})\n")

    final_summary = "\n\n".join(summaries)

    # Sending via email
    send_email("Latest AI Technology Updates", final_summary)

    # Sending to Discord
    send_to_discord(final_summary)

    print("Process completed successfully!")