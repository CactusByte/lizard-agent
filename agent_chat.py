import os
import re
import sys
import time
import requests
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool

load_dotenv()

CAPSOLVER_API_KEY = os.getenv("CAPSOLVER_API_KEY")

def solve_pump_captcha() -> str:
    """
    Uses CapSolver to solve the hCaptcha on Pump.fun and return a valid captcha token.
    """
    try:
        sitekey = "1e3d0e3e-fd0b-4b8f-95a6-6d7b6b7b7204"  # Pump.fun hCaptcha sitekey
        create_task_payload = {
            "clientKey": CAPSOLVER_API_KEY,
            "task": {
                "type": "HCaptchaTurboTask",
                "websiteURL": "https://pump.fun",
                "websiteKey": sitekey
            }
        }

        create_url = "https://api.capsolver.com/createTask"
        task_res = requests.post(create_url, json=create_task_payload).json()

        if not task_res.get("taskId"):
            raise Exception(f"Failed to create task: {task_res}")

        task_id = task_res["taskId"]
        print(f"🧠 Created CapSolver task: {task_id}")

        result_url = "https://api.capsolver.com/getTaskResult"
        while True:
            time.sleep(3)
            result_res = requests.post(result_url, json={
                "clientKey": CAPSOLVER_API_KEY,
                "taskId": task_id
            }).json()

            if result_res.get("status") == "ready":
                return result_res["solution"]["gRecaptchaResponse"]
            elif result_res.get("status") != "processing":
                raise Exception(f"Error solving captcha: {result_res}")
            print("⏳ Solving captcha...")

    except Exception as e:
        raise RuntimeError(f"❌ Captcha solving failed: {str(e)}")


@tool
def create_pump_token(prompt: str) -> str:
    """
    Creates a token on Pump.fun using provided prompt data.
    Format: 'Create token with name Yongi, ticker YNG, description best coin, image QmUC...'
    """
    try:
        # Updated regex patterns to be more flexible
        name_match = re.search(r'name\s+([A-Za-z0-9]+)', prompt)
        ticker_match = re.search(r'ticker\s+([A-Za-z0-9]+)', prompt)
        desc_match = re.search(r'description\s+(.+?)(?=image|$)', prompt)
        
        if not all([name_match, ticker_match, desc_match]):
            return "❌ Invalid input format. Please use format: 'Create token with name NAME, ticker TICKER, description DESCRIPTION'"
            
        name = name_match.group(1)
        ticker = ticker_match.group(1)
        description = desc_match.group(1).strip()
        
        # For now, using a default image hash since it's required
        image_hash = "QmUC123456789"  # This should be replaced with actual image hash

        captcha_token = solve_pump_captcha()

        payload = {
            "captchaToken": captcha_token,
            "vanityKeyCaptchaToken": captcha_token,
            "name": name,
            "ticker": ticker,
            "description": description,
            "twitter": "",
            "telegram": "",
            "website": "",
            "showName": True,
            "metadataUri": f"https://ipfs.io/ipfs/{image_hash}",
            "image": f"https://ipfs.io/ipfs/{image_hash}"
        }

        headers = {
            "Content-Type": "application/json",
            "Origin": "https://pump.fun",
            "Referer": "https://pump.fun/",
            "User-Agent": "Mozilla/5.0"
        }

        url = "https://frontend-api-v3.pump.fun/coins/create"
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 201:
            return f"✅ Token created successfully: {response.json()}"
        else:
            return f"❌ Error {response.status_code}: {response.text}"

    except Exception as e:
        return f"❌ Failed to create token: {str(e)}"


# === ✅ LLM SETUP ===
if sys.version_info >= (3, 13):
    print("⚠️ Python 3.13 may not be compatible. Use 3.9 – 3.11.")

try:
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.7
    )
except Exception as e:
    print(f"LLM error: {str(e)}")
    sys.exit(1)

# === ✅ Tavily Tool ===
try:
    tavily_tool = TavilySearchResults(api_key=os.getenv("TAVILY_API_KEY"))
except Exception as e:
    print(f"Tavily error: {str(e)}")
    sys.exit(1)

# === ✅ Agent Setup ===
try:
    agent = initialize_agent(
        tools=[tavily_tool, create_pump_token],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
        early_stopping_method="generate"
    )
except Exception as e:
    print(f"Agent setup error: {str(e)}")
    sys.exit(1)

# === ✅ Chat Loop ===
print("🤖 AI Agent ready. Ask anything or type 'exit'.\n")

while True:
    try:
        q = input("You: ").strip()
        if not q:
            continue
        if q.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        try:
            response = agent.invoke({"input": q})
            print("\nAssistant:", response["output"] if "output" in response else "❌ Couldn't parse output.")
        except Exception as e:
            print("\nAssistant: ⚠️ Error processing your request.")
            print(f"Details: {str(e)}")

    except KeyboardInterrupt:
        print("\nGoodbye!")
        break
