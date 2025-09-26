# Infinix Mobile Spec Scraper and JSON Converter

This project is an automated Python script that scrapes the latest mobile phone specifications from the official Infinix Bangladesh website. It uses Playwright for browser automation to gather product data, then leverages the z.ai chat service to parse the unstructured text into a clean JSON format. Finally, it saves the structured data into individual `.txt` files for each phone.

## Key Features

-   **Automated Link Discovery**: Automatically finds all latest product specification links from the main category page.
-   **Full-Page Text Scraping**: Navigates to each product page and extracts all visible text content.
-   **AI-Powered Data Structuring**: Feeds the scraped text to z.ai with a specific prompt to convert it into a structured JSON object.
-   **Persistent Login**: Uses a dedicated browser profile to maintain the z.ai login session, eliminating the need for repeated logins.
-   **Organized Output**: Saves the structured JSON data for each phone in a `phone_specs` directory, with filenames corresponding to the phone model.
-   **Progress Tracking**: Displays the current processing status (e.g., "Processing 5/36") in the console.

---

## How It Works

1.  **Login Setup (First-Time Only)**: The `create_login.py` script launches a browser, reads credentials from `zai_creds.txt`, and prompts the user to complete the manual login steps (like solving a captcha). This saves the session cookies in a `zai_profile` directory.
2.  **Fetch Product Links**: The main script (`infinix_latest_mobiles_data_scrape.py`) navigates to the Infinix "Latest Product" page and collects all the "View More" links that lead to the spec pages.
3.  **Scrape, Process, and Save**: For each product link, the script:
    a. Opens the page and copies all its text content.
    b. Navigates to z.ai and pastes the scraped text along with a predefined prompt.
    c. Waits for the AI to generate the JSON response and copies it.
    d. Saves the clean JSON response into a `.txt` file named after the phone model (e.g., `GT-30-Pro.txt`) inside the `phone_specs` folder.

---

## Setup and Installation

Follow these steps to set up and run the project on your local machine.

### Step 1: Prerequisites

-   [Python 3.8+](https://www.python.org/downloads/ ) installed on your system.
-   Create a file named `zai_creds.txt` in the project root. Add your z.ai email on the first line and your password on the second line.

    **Example `zai_creds.txt`:**
    ```
    example_email@mail.com
    YourSecretPassword123
    ```

### Step 2: Clone or Download the Project

Clone this repository or download all project files (`create_login.py`, `infinix_latest_mobiles_data_scrape.py`, etc.) into a single folder on your local machine.

### Step 3: Install Dependencies

1.  Open your terminal or command prompt and navigate to the project directory.
2.  Install the required Python packages using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```
3.  Install the necessary Playwright browsers (this will download browser binaries):
    ```bash
    playwright install
    ```

---

## Usage Instructions

The project requires a one-time setup for login, followed by running the main scraper.

### Step 1: Create the z.ai Login Profile (One-Time Setup)

This step saves your login session so the main script can run unattended.

1.  Run the `create_login.py` script from your terminal:
    ```bash
    python create_login.py
    ```
2.  The script will open a browser window and navigate to `chat.z.ai`. It will attempt to use the credentials from `zai_creds.txt`.
3.  **You must complete any manual login steps** in the browser, such as solving a captcha slider or other verification checks.
4.  Once you are successfully logged in, return to the terminal and press **Enter**.
5.  This will create a `zai_profile` folder in your project directory, which stores your login data.

### Step 2: Run the Main Data Scraper

After the login profile is created, you can run the main automation script.

1.  Execute the `infinix_latest_mobiles_data_scrape.py` script:
    ```bash
    python infinix_latest_mobiles_data_scrape.py
    ```
2.  The script will now run fully automatically:
    -   It will launch a browser using your saved `zai_profile`.
    -   It will find all product links from the Infinix website.
    -   It will loop through each link, scrape the data, process it with z.ai, and save the result.
3.  The final output files will be available in the `phone_specs` directory.

---

## Project Structure

```
.
├── infinix_latest_mobiles_data_scrape.py   # The main data scraping script.
├── create_login.py                         # Script for one-time z.ai login setup.
├── zai_creds.txt                           # Stores z.ai login credentials.
├── README.md                               # This documentation file.
├── requirements.txt                        # List of Python dependencies.
├── zai_profile/                            # (Generated after setup) Stores browser session data.
└── phone_specs/                            # (Generated after running) Contains the output .txt files.
```
