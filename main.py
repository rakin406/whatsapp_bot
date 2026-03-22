#!/usr/bin/env python3
"""
Usage: ./main.py <model-name> <group-link>
"""

import os
import sys
import time
import platform
import re

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from ollama import chat
from ollama import ChatResponse
from loguru import logger

# TODO: Allow user to set a custom greeting.
GREET_MESSAGE = "Hello, I am a chatbot made by Rakin Rahman. You can call me RakinBot."


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


def get_last_message(driver: ChromeDriver) -> str | None:
    messages = driver.find_elements(
        By.CSS_SELECTOR, "div.message-in span[data-testid='selectable-text']"
    )
    return messages[-1].text if messages else None


def send_message(driver: ChromeDriver, message: str):
    textarea = driver.find_element(
        By.CSS_SELECTOR,
        "#main > footer > div.x1n2onr6 > div > span > div > div > div > div.x1n2onr6 > div",
    )
    textarea.clear()

    # Filter text to retain only BMP characters
    safe_text = "".join(c for c in message if ord(c) <= 0xFFFF)

    textarea.send_keys(safe_text + Keys.ENTER)


def main():
    if len(sys.argv) <= 2:
        print("Please provide the necessary info.")
        sys.exit(1)

    model_name = sys.argv[1]
    group_link = sys.argv[2]
    code = get_group_code(group_link)
    user_data_dir = get_user_data_dir()

    if not code:
        print("Could not retrieve code")
        sys.exit(2)

    if not user_data_dir:
        print("Could not retrieve user data")
        sys.exit(3)

    # Set Chromium options
    options = Options()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory=Default")
    options.add_argument("--headless=new")  # Run headless
    options.add_argument(
        "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
    )  # Set user agent
    options.add_argument("--no-sandbox")  # Useful for containers
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--force-device-scale-factor=1")  # Ensures scaling
    options.add_argument("--enable-automation")
    options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )  # Reduces detection

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
    last_msg = ""

    while True:
        msg = get_last_message(driver)

        if not msg or msg == last_msg:
            time.sleep(1)
            continue

        response: ChatResponse = chat(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": msg,
                },
            ],
        )

        if response.message.content:
            send_message(driver, response.message.content)

        last_msg = msg
        time.sleep(1)


if __name__ == "__main__":
    main()
