#!/usr/bin/env python3
"""
Usage: ./main.py <group-link>
"""

import os
import sys
import platform
import re

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from google import genai
from loguru import logger

load_dotenv()

GREET_MESSAGE = "Hello, I am a chatbot made by Rakin Rahman. You can call me RakinBot."

PROMPT = """
You are a chatbot named RakinBot, created by Rakin Rahman.
You are friendly, casual, and funny.
Always reply to the user’s messages in a chatty, humorous way, but keep answers helpful and clear.
Feel free to add jokes, puns, or witty comments naturally, like a friend talking to you.
Keep your replies concise, engaging, and easy to read.
Only use characters in the BMP.
Remember previous messages in the conversation and refer back to them when relevant.
"""


def get_group_code(group_link: str) -> str | None:
    match = re.search(r"chat\.whatsapp\.com/([A-Za-z0-9]+)", group_link)
    return match.group(1) if match else None


def get_user_data_dir() -> str | None:
    os_name = platform.system()
    user_data_dir = None

    # Find user data path
    if os_name == "Windows":
        user_data_dir = os.path.expandvars(r"%LOCALAPPDATA%\Chromium\User Data")
    elif os_name == "Linux":
        user_data_dir = os.path.expanduser("~/.config/chromium")
    elif os_name == "Darwin":
        user_data_dir = os.path.expanduser("~/Library/Application Support/Chromium")

    return user_data_dir


def get_last_message(driver: ChromeDriver) -> str:
    messages = driver.find_elements(
        By.CSS_SELECTOR, "span[data-testid='selectable-text']"
    )
    return messages[-1].text


def send_message(driver: ChromeDriver, message: str):
    textarea = driver.find_element(
        By.CSS_SELECTOR,
        "#main > footer > div.x1n2onr6.xhtitgo.x9f619.x78zum5.x1q0g3np.xuk3077.xjbqb8w.x1wiwyrm.xquzyny.xvc5jky.x11t971q.xnpuxes.copyable-area > div > span > div > div > div > div.x1n2onr6.xh8yej3.xjdcl3y.lexical-rich-text-input > div.x1hx0egp.x6ikm8r.x1odjw0f.x1k6rcq7.x6prxxf",
    )
    textarea.clear()
    textarea.send_keys(message + Keys.ENTER)


def main():
    if len(sys.argv) <= 1:
        print("Please give the group link.")
        sys.exit(1)

    group_link = sys.argv[1]
    code = get_group_code(group_link)
    user_data_dir = get_user_data_dir()

    if not code:
        print("Could not retrieve code")
        sys.exit(2)

    if not user_data_dir:
        print("Could not retrieve user data")
        sys.exit(3)

    # Create Gemini client
    logger.debug("Initializing Gemini chat session")
    client = genai.Client()
    chat = client.chats.create(
        model="gemini-3-flash-preview",
        history=[{"role": "user", "parts": [{"text": PROMPT}]}],
    )
    logger.info("Initialized Gemini chat session")

    # Set Chromium options
    options = Options()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory=Default")
    options.add_argument("--headless=new")  # Run headless
    options.add_argument("--no-sandbox")  # Useful for containers
    options.add_argument("--disable-gpu")

    # Open Chromium
    logger.debug("Initializing ChromeDriver")
    driver = webdriver.Chrome(options=options)
    logger.info("Initialized ChromeDriver")

    driver.implicitly_wait(10)

    # Open whatsapp group chat
    logger.debug("Opening chat")
    chat_url = f"https://web.whatsapp.com/accept?code={code}"
    driver.get(chat_url)
    logger.info("Opened chat")

    # Greet
    send_message(driver, GREET_MESSAGE)
    logger.info("Sent greet message")
    last_msg = GREET_MESSAGE

    while True:
        msg = get_last_message(driver)
        if msg == last_msg:
            continue

        response = chat.send_message(msg)

        if response.text:
            send_message(driver, response.text)

        last_msg = msg


if __name__ == "__main__":
    main()
