import pandas as pd
import schedule
import time
from datetime import datetime
from autanimos_agent.agent import  run_agent

import asyncio
# === Function to run for each matching row ===
async def run_task(row):

    prompt = f"""
    Title: {row['title']}
    Goal: {row['goal']}
    Short explanation: {row['short explanation']}
    minimum words: 700
    SEO optimization: yes
    language: Persian
    output format: html
    """
    result = await run_agent(prompt)
    print(result)

# === Function to check today's items ===
def check_today_tasks():
    # Load Excel file (update file name/path if needed)
    df = pd.read_excel("content-planer.xlsx")
    
    # Ensure consistent date format (handles strings like "11/12/25")
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
    
    today = datetime.now().date()
    today_tasks = df[df['date'] == today]

    if today_tasks.empty:
        print(f"No tasks for today ({today}).")
    else:
        print(f"Tasks for today ({today}):")
        for _, row in today_tasks.iterrows():
            asyncio.run(run_task(row))

# === Schedule to run every day at 09:00 ===
schedule.every().day.at("09:00").do(check_today_tasks)
# schedule.every().second.do(check_today_tasks)

# === Keep running ===
print("Scheduler started. Waiting for next run...")
while True:
    schedule.run_pending()
    time.sleep(30)