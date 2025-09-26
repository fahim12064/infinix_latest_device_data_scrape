from playwright.sync_api import sync_playwright
import pyperclip
import time

def get_full_text_ctrl_a(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(5)  # পেজ পুরো লোড হওয়ার জন্য অপেক্ষা

        # Ctrl + A চাপা (সব সিলেক্ট হবে)
        page.keyboard.press("Control+A")
        time.sleep(1)

        # Ctrl + C চাপা (কপি হবে)
        page.keyboard.press("Control+C")
        time.sleep(1)

        # এখন ক্লিপবোর্ড থেকে পড়া
        full_text = pyperclip.paste()

        # এক লাইনে কনভার্ট করা
        one_line_text = " ".join(full_text.split())

        browser.close()
        return one_line_text

# Example usage
url = "https://bd.infinixmobility.com/specs/note-50-pro"
data = get_full_text_ctrl_a(url)
print(data)
