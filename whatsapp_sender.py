import os
import sys
import time
import subprocess

# Ensure UTF-8 output so emojis and special characters never crash Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ================= Configuration =================
GROUP_NAME = "THE BOYS 🗿"
SEARCH_KEYWORD = "BOYS"
MESSAGE = "Hello Guys"
COUNT = 50
DELAY = 0.1  # Delay between messages in seconds

PROFILE_DIR = os.path.abspath("./whatsapp_profile")
# =================================================

def release_stale_locks(profile_path):
    """Clean up any lingering background Chrome process locks."""
    lockfile = os.path.join(profile_path, "lockfile")
    if os.path.exists(lockfile):
        try:
            with open(lockfile, "a"):
                pass
        except PermissionError:
            print("Releasing background Chrome locks...")
            subprocess.run(["taskkill", "/F", "/IM", "chrome.exe", "/IM", "chromedriver.exe"], capture_output=True)
            time.sleep(2)

release_stale_locks(PROFILE_DIR)

options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={PROFILE_DIR}")
options.add_argument("--remote-allow-origins=*")
options.page_load_strategy = "eager"

print("Starting Chrome...")
driver = webdriver.Chrome(options=options)

try:
    print("Navigating to WhatsApp Web...")
    driver.get("https://web.whatsapp.com/")

    wait = WebDriverWait(driver, 120)

    print("Waiting for WhatsApp Web to load...")
    # Wait for either the chat pane or search bar to be present
    wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            '//div[@id="pane-side"] | //input[contains(@aria-label, "Search")] | //div[@role="textbox"]'
        ))
    )
    print("WhatsApp Web is ready!")
    time.sleep(2)

    # 1. Check if the group is already visible in the recent chat list
    group_xpath = (
        f'//span[@title="{GROUP_NAME}"] | '
        f'//span[contains(@title, "{SEARCH_KEYWORD}")] | '
        f'//span[contains(text(), "{SEARCH_KEYWORD}")]'
    )
    chats = driver.find_elements(By.XPATH, group_xpath)

    if chats:
        print(f"Found '{GROUP_NAME}' directly in recent chats! Opening...")
        # Click the chat element or its parent clickable container
        driver.execute_script("arguments[0].scrollIntoView(true);", chats[0])
        time.sleep(0.5)
        chats[0].click()
    else:
        # 2. If not visible directly, search for it
        print(f"Searching for '{SEARCH_KEYWORD}'...")
        search_input = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                '//input[contains(@aria-label, "Search")] | '
                '//input[contains(@placeholder, "Search")] | '
                '//div[@id="side"]//div[@contenteditable="true"]'
            ))
        )
        search_input.click()
        time.sleep(0.5)
        search_input.send_keys(Keys.CONTROL + "a")
        search_input.send_keys(Keys.BACKSPACE)
        search_input.send_keys(SEARCH_KEYWORD)
        time.sleep(2)

        # Click the first matching search result
        print("Selecting group from search results...")
        try:
            match = wait.until(EC.element_to_be_clickable((By.XPATH, group_xpath)))
            match.click()
        except Exception:
            search_input.send_keys(Keys.ENTER)

    time.sleep(2)

    # 3. Locate the message input box in the footer
    print("Locating message box...")
    message_box = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            '//footer//div[@contenteditable="true"][@role="textbox"] | //footer//div[@contenteditable="true"]'
        ))
    )
    print("Group chat opened! Starting to send messages...\n")

    # JavaScript to instantly insert text and click the send button
    fast_send_script = """
        const box = arguments[0];
        const text = arguments[1];
        box.focus();
        document.execCommand('insertText', false, text);
        const btn = document.querySelector('footer button[aria-label="Send"], footer span[data-icon="send"]');
        if (btn) {
            (btn.closest('button') || btn).click();
            return true;
        }
        return false;
    """

    # Focus message box once before starting the burst
    message_box.click()
    time.sleep(0.3)

    print(f"⚡ Firing {COUNT} message(s) at lightning speed...")
    start_time = time.time()

    for i in range(COUNT):
        sent = driver.execute_script(fast_send_script, message_box, MESSAGE)
        if not sent:
            message_box.send_keys(Keys.ENTER)

        print(f"[{i + 1}/{COUNT}] Sent: '{MESSAGE}'")
        if DELAY > 0:
            time.sleep(DELAY)

    duration = time.time() - start_time
    print(f"\n⚡ All {COUNT} messages sent in {duration:.2f} seconds ({COUNT / max(duration, 0.001):.1f} msgs/sec)!")

except Exception as e:
    print(f"\nAn error occurred: {e}")

finally:
    print("\n-----------------------------------------------------------")
    try:
        input("Press Enter here in this terminal to close Chrome cleanly...")
    except Exception:
        time.sleep(3)
    print("Closing browser...")
    driver.quit()
