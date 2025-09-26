import os
import json
import re
from openai import OpenAI

# -----------------------
# Configuration
# -----------------------
# আপনার দেওয়া নতুন API কী এখানে ব্যবহার করা হয়েছে।
OPENROUTER_API_KEY = "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"

# OpenRouter এর জন্য OpenAI ক্লায়েন্ট সেটআপ করা
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


def convert_specs_to_json_with_ai(text_specs: str) -> dict:
    """
    DeepSeek AI মডেল ব্যবহার করে টেক্সট স্পেসিফিকেশনকে JSON ফরম্যাটে রূপান্তর করে।
    """
    json_format_template = """
    {
      "Design": {
        "Dimensions:": "...",
        "Weight:": "...",
        "Materials:": "...",
        "Resistance:": "...",
        "Biometrics:": "...",
        "Colors:": "..."
      },
      "Display": {
        "Size:": "...",
        "Resolution:": "...",
        "Technology:": "...",
        "Refresh rate:": "...",
        "Screen-to-body:": "...",
        "Peak brightness:": "...",
        "Features:": "..."
      },
      "Hardware": {
        "Device type:": "Smartphone",
        "OS:": "...",
        "Processor:": "...",
        "GPU:": "...",
        "RAM:": "...",
        "Internal storage:": "..."
      },
      "Battery": {
        "Capacity:": "...",
        "Type:": "...",
        "Charging:": "...",
        "Max charge speed:": "..."
      },
      "Camera": {
        "Rear:": "...",
        "Main camera:": "...",
        "Second camera:": "...",
        "Third camera:": "...",
        "Flash:": "...",
        "Front:": "...",
        "Video recording:": "..."
      },
      "Cellular": {
        "5G:": "...",
        "SIM type:": "..."
      },
      "Multimedia": {
        "Headphones:": "...",
        "Speakers:": "...",
        "Screen mirroring:": "...",
        "Additional microphone(s)": "..."
      },
      "Connectivity & Features": {
        "Bluetooth:": "...",
        "Wi-Fi:": "...",
        "USB:": "...",
        "Location:": "...",
        "Sensors:": "...",
        "Other:": "..."
      }
    }
    """

    system_prompt = f"""
    You are an expert data extraction AI. Your task is to read the provided raw text containing mobile phone specifications and convert it into a structured JSON object.
    You must follow this exact JSON format and fill in the values based on the text.
    If a value is not found in the text, you must use an empty string "" or "Not specified".
    Do not add any extra text, explanations, or markdown. Your output must be ONLY the JSON object.

    Here is the JSON format you must follow:
    {json_format_template}
    """

    try:
        print("AI মডেলের কাছে ডেটা পাঠানো হচ্ছে...")
        completion = client.chat.completions.create(
            # --- সমস্যার সমাধান: সঠিক মডেলের নাম ব্যবহার করা হয়েছে ---
            model="deepseek/deepseek-chat-v3.1:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Here is the phone specification text:\n\n{text_specs}"},
            ],
            temperature=0.1,
        )

        ai_response = completion.choices[0].message.content
        print("AI মডেল থেকে সফলভাবে রেসপন্স পাওয়া গেছে।")

        json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
        if not json_match:
            raise ValueError("AI did not return a valid JSON object.")

        clean_json_str = json_match.group(0)
        return json.loads(clean_json_str)

    except Exception as e:
        print(f"একটি ত্রুটি ঘটেছে: {e}")
        return None


# --- Main Execution Block ---
if __name__ == "__main__":
    input_text = """
Smartphones
Accessories
Laptops
Tablets
XOS
NOTE 50 Pro+ 5G
Overview
Specs
Buy now

NOTE 50 Pro+ 5G

Ultra-Resilient ArmorAlloy™ Metal Frame Performance Design

100X Periscope Camera | SONY IMX896 OIS Night Master Camera

100W All-Round FastCharge3.0 | 50W Wireless MagCharge

4nm MediaTek Dimensity 8350 Ultimate 5.5G Chipset

144Hz 6.78'' AMOLED Display | In-Display Fingerprint

One-Tap Infinix AI♾️


Size & Weight


Size and Weight

MODEL

X6856

DIMENSION

163.36 x 74.53 x7.99mm

WEIGHT

209g

COLOUR

Titanium Grey/Enchanted Purple/Racing Edition


*Product size, product weight and related specifications are theoretical values only. Actual measurements between individual products may vary. All specifications are subject to the actual product

PLATFORM

CHIPSET

MediaTek Dimensity 8350 Ultimate

CPU

Octa-core (4*Cortex-A510 up to 2.2Ghz & 4*Cortex-A715 up to 3.35Ghz)

GPU

Mali-G615 MC6

PROCESS

4nm

NETWORK

TECHNOLOGY

5.5G/5G/4G/3G/2G

BANDWIDTH*

2G: B2|3|5|8

3G: B1|2|4|5|8

4G: FDD B1|2|3|4|5|7|8|12|17|20|28|66 - TDD: 38|40|41|42

5G: sub6 FDD n1|3|5|7|8|12|20|28|66|71 - TDD: n38|40|41|77|78


*Bandwidth availability and connectivity can vary depending on region and local service provider.

CAMERA

REAR

50MP OIS+50MP OIS+8MP

FRONT

32MP, f/2.2, FOV 88.9°, FF

FLASH

Rear Dual Flash

SCENE MODES

Vlog, Video, AI Cam, Portrait, Super Night, Slow Motion,

Time-Lapse, Dual Video, Short Video, Sky Shop, Pro, Panorama,

Documents, Long-exposure，AIGC Portrait, Street Snap

VIDEO RECORDING

Front: 4K 30FPS/1080P30FPS/1080P 60FPS

Rear: 4K 30FPS/4K 60FPS /1080P 30FPS/1080P 60FPS

Slow Motion: 1080P 120FPS/1080P 240FPS

MEMORY

ROM & RAM

256GB ROM + 12GB RAM + 12GB Extended RAM

TYPE

UFS4.0 + LPDDR5X

SENSORS & TOOLS

G-SENSOR

YES

E-COMPASS

YES

GYROSCOPE

YES

LIGHT SENSOR

YES

PROXIMITY SENSOR

YES

FINGERPRINT

YES, IN-DISPLAY FINGERPRINT

MOTOR

YES, X-Axis Motor

INFRARED BLASTER

YES


*Tested under IEC 60529 standard. Physical damage, daily wear and tear, and/or need for disassembly may cause ingress protection to deteriorate. Submersion in liquid and the resulting damage is not covered by the warranty.

MULTIMEDIA

AUDIO PLAYBACK*

MP3, FLAC, OGG, OGA,WAV, AAC, AMR, AWB, APE, MIDI

VIDEO PLAYBACK*

MP4, MKV, TS, 3GP, WEBM

OTHER FEATURES

Audio: Dual Speakers, JBL, Hi-Res Audio,Hi-Res Wireless Audio, DTS Video: DRM Widvine L1


*Listed playback information are for reference only. Decoding formats of source files can influence playback support.

BATTERY

CAPACITY (TYP)

5200mAh (TYP)

CHARGING*

Max 100W, 20V/5A

REVERSE CHARGING*

YES, Max 10W


*Different voltage inputs may affect maximum output power in some regions.

CONNECTION

SIM CARD SLOT

DUAL NANO SIM

GPS NAVIGATION

YES

WIFI(WLAN)

IEEE 802.11 a/b/g/n/ac/ax （WIFI 6）

BLUETOOTH

BLUETOOTH 5.4

USB PORT

USB TYPE-C

OTG

YES

EARPHONE

YES, TYPE-C

FM

YES

NFC

YES

DISPLAY

SIZE

6.78-INCHES

SCREEN-TO-BODY RATIO

93.4%

REFRESH RATE

60/120/144Hz

RESOLUTION

FHD+ 1080*2436

MATERIAL

AMOLED

PEAK BRIGHTNESS

550 nits (TYP), 1000 nits (HBM Brightness), 1300 nits (Peak Brightness)

COLOR GAMUT

100% DCI-P3

INSTANT TOUCH SAMPLING RATE

2160Hz

TOUCH SAMPLING RATE

UP TO 240Hz

PWM DIMMING

UP TO 2304Hz

OTHER FEATURES

Always-On Display

SPLASH, WATER, & DUST RESISTANCE

IP64

OPERATING SYSTEM

XOS 15




ABOUT US
Our Story
Contact Us
PRODUCTS
Smartphones
CARE
Repair Center
Limited Warranty
SERVICE
Find a Store
XOS
Infinix © 2025 All rights reserved
Privacy Policy
Terms of use
Location:
Bangladesh(EN)
    """

    structured_data = convert_specs_to_json_with_ai(input_text)

    if structured_data:
        output_filename = "ai_generated_specs.json"
        with open(output_filename, 'w', encoding='utf-8') as json_file:
            json.dump(structured_data, json_file, indent=2, ensure_ascii=False)

        print(f"\nসফলভাবে '{output_filename}' ফাইলটি তৈরি করা হয়েছে।")

        print("\n--- AI দ্বারা তৈরি করা JSON ---")
        print(json.dumps(structured_data, indent=2, ensure_ascii=False))
