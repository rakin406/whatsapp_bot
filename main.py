#!/usr/bin/env python3
"""
Usage: ./main.py <group-link>
"""

import os
import sys
import platform
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from loguru import logger


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

    options = Options()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory=Default")
    options.add_experimental_option("detach", True)

    # Open chrome
    logger.debug("Initializing ChromeDriver")
    driver = webdriver.Chrome(options=options)
    logger.info("Initialized ChromeDriver")

    driver.implicitly_wait(10)

    # Go to whatsapp link
    logger.debug("Navigating to link")
    driver.get(group_link)
    logger.info("Navigated to link")

    # Quit chrome
    # logger.debug("Stopping ChromeDriver")
    # driver.quit()
    # logger.info("Stopped ChromeDriver")


if __name__ == "__main__":
    main()
