# ⚡ Automate WhatsApp Message Sender

An automated, ultra-fast WhatsApp Web message automation tool built using **Python** and **Selenium WebDriver**. It allows you to automate sending customized messages to individuals or groups with persistent login session support, DOM-level message injection, and automatic process lock handling.

---

## 📌 Features

- **⚡ High-Speed Message Delivery:** Uses client-side JavaScript DOM injection (`execCommand('insertText')`) to send messages rapidly without sluggish manual typing delays.
- **💾 Persistent Login Session:** Saves your session in a dedicated Chrome profile directory (`./whatsapp_profile`), meaning you only have to scan the QR code once!
- **🔍 Smart Contact / Group Detection:** Searches active chats first and automatically falls back to search queries if the conversation isn't in recent view.
- **🛡️ Stale Lock Recovery:** Automatically detects and clears lingering Chrome background processes or locks on Windows before launching.
- **🌐 UTF-8 & Emoji Support:** Reconfigures console standard I/O to handle emojis, symbols, and non-ASCII character encoding gracefully.
- **⏱️ Configurable Delays & Counts:** Customize message payload, loop count, and throttle delays according to your needs.

---

## 📋 Prerequisites

Before running the script, ensure you have the following installed on your machine:

1. **Python 3.8+**
   - Verify installation:
     ```bash
     python --version
     ```
2. **Google Chrome Browser**
   - Ensure standard Google Chrome is installed on your computer.
   - *Note:* Selenium 4+ automatically manages ChromeDriver via Selenium Manager; you do not need to download or place `chromedriver.exe` manually.
3. **Active WhatsApp Account**
   - Your smartphone must be connected to the internet to scan the QR code on initial login.

---

## 🚀 Installation & Setup

### 1. Clone or Download the Repository

```bash
git clone https://github.com/mrifadh27/Automate_Whatsapp_MSG.git
cd Automate_Whatsapp_MSG
```

### 2. (Optional) Create a Virtual Environment

It is recommended to use a virtual environment:

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install the required packages using the provided [requirements.txt](file:///c:/Users/MSI/Desktop/Whatsapp/requirements.txt):

```bash
pip install -r requirements.txt
```

*(Alternatively: `pip install selenium`)*

---

## ⚙️ Configuration

Open [whatsapp_sender.py](file:///c:/Users/MSI/Desktop/Whatsapp/whatsapp_sender.py) in your text editor and modify the configuration variables at the top of the file:

```python
# ================= Configuration =================
GROUP_NAME = "THE BOYS 🗿"        # Exact chat or group title
SEARCH_KEYWORD = "BOYS"           # Keyword used if chat is not in recent list
MESSAGE = "Hello from automation!" # The message content to send
COUNT = 50                        # Number of times to send the message
DELAY = 0.5                       # Delay between messages in seconds (e.g., 0.1 - 1.0)

PROFILE_DIR = os.path.abspath("./whatsapp_profile") # Chrome profile directory
# =================================================
```

### Configuration Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `GROUP_NAME` | `str` | Exact name of the contact or group as it appears in WhatsApp. |
| `SEARCH_KEYWORD` | `str` | Partial keyword used to search for the chat in WhatsApp's search bar. |
| `MESSAGE` | `str` | The text content to be sent. Supports emojis and special characters. |
| `COUNT` | `int` | Total number of messages to deliver. |
| `DELAY` | `float` | Delay (in seconds) between successive messages. Recommended: `0.5`s or higher for safety. |
| `PROFILE_DIR` | `str` | Absolute path to store Chrome user session data so you stay logged in. |

---

## 🏃 How to Run

### Step 1: Launch the Script

Execute the script from your terminal:

```bash
python whatsapp_sender.py
```

### Step 2: First-Time Login (Scan QR Code)

- On the very first run, Google Chrome will open and navigate to `https://web.whatsapp.com/`.
- Open **WhatsApp** on your mobile phone:
  - Tap **Menu / Settings** (⋮ or gear icon) > **Linked Devices** > **Link a Device**.
  - Point your phone camera at the QR code displayed in the Chrome window.
- Once authenticated, WhatsApp Web will load your chats.

> [!NOTE]
> The login session is saved into the `./whatsapp_profile` directory. You will **not** need to scan the QR code on subsequent runs unless you log out or delete the profile folder.

### Step 3: Automated Sending

- The script detects the group or contact (via recent chats or search).
- It focuses the input box and begins sending the configured `MESSAGE` for `COUNT` iterations.
- Real-time progress and delivery speed metrics will be printed to your terminal.

### Step 4: Clean Exit

- When all messages are sent, the terminal will prompt:
  ```
  Press Enter here in this terminal to close Chrome cleanly...
  ```
- Press <kbd>Enter</kbd> to properly shut down ChromeDriver and release Chrome profile locks.

---

## 📂 Project Structure

```
Automate_Whatsapp_MSG/
│
├── whatsapp_sender.py     # Main automation script
├── requirements.txt       # Python dependencies (Selenium)
├── README.md              # Project documentation and run guide
└── whatsapp_profile/      # Local Chrome user data profile (session cache)
```

---

## 🛠️ Troubleshooting & Tips

### 1. Chrome Stale Lock / Session Not Starting
- **Symptom:** Error stating that the user data directory is in use.
- **Fix:** The script contains `release_stale_locks()` which terminates lingering Chrome processes on Windows. If needed, manually close all open Chrome windows or run:
  ```powershell
  taskkill /F /IM chrome.exe /IM chromedriver.exe
  ```

### 2. Group or Contact Not Found
- **Symptom:** Script times out waiting for the contact.
- **Fix:** Ensure `GROUP_NAME` matches the contact/group name exactly (including emojis, spaces, or capitalization), or provide an accurate `SEARCH_KEYWORD`. Ensure the chat exists and is not archived.

### 3. Avoiding WhatsApp Bans / Rate Limiting
- **Caution:** Sending high volumes of messages in rapid succession (e.g., hundreds of messages with `DELAY = 0.05`) may trigger WhatsApp's automated spam detection and lead to account bans or temporary suspension.
- **Recommendation:** Keep `DELAY` at `0.5` seconds or higher, and use reasonable message counts.

### 4. Console Encoding Errors on Windows
- If you notice emojis displaying as `?` or crashes on older Windows command prompts, run the script inside **Windows Terminal**, **PowerShell**, or **VS Code Integrated Terminal**.

---

## ⚠️ Disclaimer

This project is for **educational, testing, and personal productivity purposes only**. 

Automated messaging must comply with [WhatsApp's Terms of Service](https://www.whatsapp.com/legal/terms-of-service). The author is not responsible for any misuse, account suspensions, or bans resulting from the use of this software. Do not use this tool for spamming or unsolicited advertising.
