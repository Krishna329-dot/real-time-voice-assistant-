import subprocess
import webbrowser
import psutil
import time
import pyautogui
import os

def bring_window_front():
    time.sleep(1)
    pyautogui.hotkey("alt", "tab")

def safe_system_action(action: str, query: str | None = None) -> str:

    if action == "cpu_status":
        return f"🧠 CPU usage is {psutil.cpu_percent()}%"

    if action == "open_notepad":
        subprocess.Popen(["notepad.exe"])
        bring_window_front()
        return "✅ Notepad opened on screen"

    if action == "open_chrome":
        webbrowser.open("chrome://newtab")
        bring_window_front()
        return "✅ Chrome opened on screen"

    if action == "open_youtube":
        webbrowser.open("https://www.youtube.com")
        bring_window_front()
        return "✅ YouTube opened on screen"

    if action == "youtube_search":
        if not query:
            return "❌ Search query missing"

        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        bring_window_front()

        return f"▶️ YouTube search opened for {query}"

    return "❌ Action not allowed"
