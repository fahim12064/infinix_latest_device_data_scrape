from playwright.sync_api import sync_playwright
from time import sleep

PROFILE_DIR = "C:/All_data/zai_profile"
phone_data = input("input the data: ")

with sync_playwright() as p:
    # Launch browser with profile
    print("Launching browser...")
    browser = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        headless=False,
        args=["--disable-blink-features=AutomationControlled"]
    )
    page = browser.new_page()
    print("Browser ready.")

    try:
        # --- Step 3: Navigate to website and wait for chat interface ---
        print("Navigating to https://chat.z.ai/...")
        page.goto("https://chat.z.ai/", timeout=60000, wait_until="domcontentloaded")

        # Wait for chat input box to load
        page.wait_for_selector("textarea#chat-input", timeout=30000)
        print("Chat interface loaded.")

        # --- Step 5: Send prompt for outline generation ---
        instruction = """You are a professional data extraction AI.  
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
            "Rear:": "",
            "Flash:": "",
            "Front:": "",
            "Video recording:": "",
            "Scene modes:": ""
          },
          "Design": {
            "Colors:": "",
            "Dimensions:": "",
            "Weight:": "",
            "Biometrics:": "",
            "Resistance:": "",
            "Materials:": ""
          },
          "Battery": {
            "Capacity:": "",
            "Charging:": "",
            "Reverse charging:": "",
            "Wireless charging:": ""
          },
          "Display": {
            "Size:": "",
            "Screen-to-body:": "",
            "Refresh rate:": "",
            "Resolution:": "",
            "Technology:": "",
            "Peak brightness:": "",
            "Color gamut:": "",
            "Touch sampling rate:": "",
            "PWM Dimming:": "",
            "Other features:": ""
          },
          "Cellular": {
            "Technology:": "",
            "2G bands:": "",
            "3G bands:": "",
            "4G bands:": "",
            "5G bands:": "",
            "SIM type:": ""
          },
          "Hardware": {
            "OS:": "",
            "Chipset:": "",
            "CPU:": "",
            "GPU:": "",
            "Process:": "",
            "RAM:": "",
            "Internal storage:": "",
            "Memory type:": ""
          },
          "Multimedia": {
            "Audio playback:": "",
            "Video playback:": "",
            "Speakers:": "",
            "Video features:": "",
            "Headphones:": ""
          },
          "Connectivity & Features": {
            "GPS:": "",
            "Wi-Fi:": "",
            "Bluetooth:": "",
            "USB:": "",
            "OTG:": "",
            "FM:": "",
            "NFC:": "",
            "Sensors:": "",
            "Other features:": ""
          }
        }

        ---

        Now, here is the smartphone specification text.  
        Read it carefully and generate the JSON object strictly in the above format:  

        here is the phone details...."""

        final_prompt = f"{instruction} {phone_data}"

        chat_input_selector = "textarea#chat-input"

        print(f"Typing prompt: '{final_prompt[:60]}...'")
        page.fill(chat_input_selector, final_prompt)
        page.press(chat_input_selector, "Enter")
        print("Prompt sent! Waiting for AI response...")

        # --- Step 6: Copy AI response ---
        print("Preparing to copy AI response...")
        # Wait for visible "Copy" button (max 10 minutes)
        page.wait_for_selector("button.copy-response-button:visible", timeout=600000)

        # Find the last visible "Copy" button
        final_copy_button = page.locator("button.copy-response-button:visible").last

        # Wait for button to be fully loaded
        final_copy_button.wait_for(state="attached", timeout=600000)
        final_copy_button.wait_for(state="visible", timeout=600000)

        sleep(2)  # Brief pause for large responses

        # Click button to copy response
        final_copy_button.click()
        print("AI response copied to clipboard.")

        sleep(1)  # Brief pause for clipboard processing

    except Exception as e:
        print(f"Unexpected error occurred: {e}")
    finally:
        # --- Step 7: Close program ---
        print("Task completed. Browser will remain open.")
        input("Press Enter in this console to close the browser...")
        browser.close()
        print("Browser closed.")


