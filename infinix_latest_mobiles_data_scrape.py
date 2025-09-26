import time
import json
from playwright.sync_api import sync_playwright, Page
from pathlib import Path

# --- Configuration ---
# URL for the main product category page
MAIN_PRODUCT_URL = "https://bd.infinixmobility.com/category/8?cId=15&cName=Latest%20Product"
# Base URL for the spec pages (since the scraped links are relative )
BASE_SPECS_URL = "https://bd.infinixmobility.com/specs"
# Path to your Chrome profile for z.ai login
ZAI_PROFILE_DIR = "zai_profile"
# Directory to save the final text files
OUTPUT_DIR = "phone_specs"

# --- Z.ai Prompt Template ---
# This is the instruction template you provided for z.ai
ZAI_INSTRUCTION_PROMPT = """
You are a professional data extraction AI.  
Your task is to read smartphone specifications from messy or unstructured text and convert them into a clean JSON format.  

⚠️ Very Important Instructions:
- Follow the exact JSON format given below.
- Extract only relevant values for each field.
- If a value is missing, write "Not specified".
- Do not add extra commentary, explanation, or markdown. 
- Only return the JSON object.

Here is the JSON format you must follow:

{
  "Camera": {
    "Rear:": "", "Flash:": "", "Front:": "", "Video recording:": "", "Scene modes:": ""
  },
  "Design": {
    "Colors:": "", "Dimensions:": "", "Weight:": "", "Biometrics:": "", "Resistance:": "", "Materials:": ""
  },
  "Battery": {
    "Capacity:": "", "Charging:": "", "Reverse charging:": "", "Wireless charging:": ""
  },
  "Display": {
    "Size:": "", "Screen-to-body:": "", "Refresh rate:": "", "Resolution:": "", "Technology:": "", "Peak brightness:": "", "Color gamut:": "", "Touch sampling rate:": "", "PWM Dimming:": "", "Other features:": ""
  },
  "Cellular": {
    "Technology:": "", "2G bands:": "", "3G bands:": "", "4G bands:": "", "5G bands:": "", "SIM type:": ""
  },
  "Hardware": {
    "OS:": "", "Chipset:": "", "CPU:": "", "GPU:": "", "Process:": "", "RAM:": "", "Internal storage:": "", "Memory type:": ""
  },
  "Multimedia": {
    "Audio playback:": "", "Video playback:": "", "Speakers:": "", "Video features:": "", "Headphones:": ""
  },
  "Connectivity & Features": {
    "GPS:": "", "Wi-Fi:": "", "Bluetooth:": "", "USB:": "", "OTG:": "", "FM:": "", "NFC:": "", "Sensors:": "", "Other features:": ""
  }
}

---

Now, here is the smartphone specification text.  
Read it carefully and generate the JSON object strictly in the above format:  

here is the phone details....
"""


def get_all_product_spec_links(page: Page) -> list[str]:
    """Navigates to the main product page and scrapes all spec links."""
    print(f"Navigating to product list: {MAIN_PRODUCT_URL}")
    page.goto(MAIN_PRODUCT_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(10000)  # Wait for dynamic content to load

    view_more_anchors = page.locator('a:has-text("View More")')
    count = view_more_anchors.count()

    if count == 0:
        print("No 'View More' links found. The website structure might have changed.")
        return []

    print(f"Found {count} 'View More' links. Extracting URLs...")
    all_hrefs = [view_more_anchors.nth(i).get_attribute('href') for i in range(count)]

    # Filter out any None values and create full URLs
    final_links = [BASE_SPECS_URL + href for href in all_hrefs if href]

    print("\n--- Found Product Spec Links ---")
    for i, link in enumerate(final_links):
        print(f"{i + 1}: {link}")
    print("--------------------------------\n")

    return final_links


def scrape_text_from_page(page: Page, url: str) -> str:
    """Goes to a URL, selects all text, and returns it as a single line."""
    print(f"Scraping text from: {url}")
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_timeout(5000)  # Wait for the page to fully render

    # Use JavaScript to get all body text, which is more reliable than simulating key presses
    full_text = page.evaluate("document.body.innerText")

    # Convert to a single line by replacing newlines and multiple spaces
    one_line_text = " ".join(full_text.split())
    print("Successfully scraped and formatted text into one line.")
    return one_line_text


def get_spec_json_from_zai(page: Page, phone_data: str) -> str:
    """Pastes the phone data into z.ai and copies the resulting JSON."""
    print("Navigating to z.ai...")
    page.goto("https://chat.z.ai/", timeout=60000, wait_until="domcontentloaded")

    chat_input_selector = "textarea#chat-input"
    page.wait_for_selector(chat_input_selector, timeout=30000)
    print("z.ai chat interface loaded.")

    final_prompt = f"{ZAI_INSTRUCTION_PROMPT} {phone_data}"

    print("Pasting prompt into z.ai...")
    page.fill(chat_input_selector, final_prompt)
    page.press(chat_input_selector, "Enter")
    print("Prompt sent! Waiting for AI response...")

    # Wait for the last visible "Copy" button to appear (10-minute timeout for long responses)
    copy_button_selector = "button.copy-response-button:visible"
    page.wait_for_selector(copy_button_selector, timeout=600000)
    final_copy_button = page.locator(copy_button_selector).last

    # A short, reliable pause before clicking the copy button
    time.sleep(3)

    # Use JavaScript to get the clipboard content directly after click
    # This is more reliable than relying on an external library like pyperclip
    page.evaluate("navigator.clipboard.writeText('')")  # Clear clipboard first
    final_copy_button.click()

    # Wait a moment for the clipboard to be populated
    time.sleep(1)

    ai_response = page.evaluate("navigator.clipboard.readText()")
    print("AI response copied successfully.")
    return ai_response


def main():
    """Main function to run the complete automation workflow."""
    # Create the output directory if it doesn't exist
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    with sync_playwright() as p:
        # Launch a persistent browser context to use your logged-in z.ai profile
        print("Launching browser with persistent profile...")
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=ZAI_PROFILE_DIR,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser_context.new_page()
        print("Browser ready.")

        try:
            # --- Step 1: Get all product links ---
            product_links = get_all_product_spec_links(page)

            if not product_links:
                print("No product links found to process. Exiting.")
                return

            # --- Step 2, 3, 4: Loop through each link, scrape, and process with AI ---
            total_links = len(product_links)
            for i, link in enumerate(product_links, start=1):  # Use enumerate, start counting from 1
                try:
                    # The new print statement with the counter
                    print(f"\n--- Processing {i}/{total_links} Product: {link} ---")

                    # Step 2: Scrape all text from the product page
                    one_line_text = scrape_text_from_page(page, link)

                    if not one_line_text.strip():
                        print("Warning: Scraped text is empty. Skipping this product.")
                        continue

                    # Step 3: Get the JSON data from z.ai
                    json_response = get_spec_json_from_zai(page, one_line_text)

                    # Step 4: Save the response to a file
                    phone_name = link.split('/')[-1].replace('%2B', '+') or "unknown-phone"
                    file_path = Path(OUTPUT_DIR) / f"{phone_name}.txt"

                    if json_response.strip().startswith("```json"):
                        json_response = json_response.replace("```json", "").replace("```", "").strip()

                    with open(file_path, 'w', encoding='utf-8') as f:
                        try:
                            parsed_json = json.loads(json_response)
                            f.write(json.dumps(parsed_json, indent=2))
                            print(f"Successfully saved formatted JSON to: {file_path}")
                        except json.JSONDecodeError:
                            f.write(json_response)
                            print(f"Warning: AI response was not valid JSON. Saved as plain text to: {file_path}")

                except Exception as e:
                    print(f"!!!!!!!! An error occurred while processing {link}: {e} !!!!!!!!")
                    print("Moving to the next product...")

        finally:
            print("\n--- Automation Complete ---")
            input("Press Enter in this console to close the browser...")
            browser_context.close()
            print("Browser closed.")

if __name__ == "__main__":
    main()
