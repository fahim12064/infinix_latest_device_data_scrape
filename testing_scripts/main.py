from playwright.sync_api import sync_playwright
url = "https://bd.infinixmobility.com/category/8?cId=15&cName=Latest%20Product"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_timeout(15000)
    view_more_anchors = page.locator('a:has-text("View More")')
    count = view_more_anchors.count()
    if count == 0:
        print("No 'View More' links found on the page.")

    print(f"Found {count} 'View More' links. Extracting URLs...")

    all_hrefs = []
    for i in range(count):
        anchor = view_more_anchors.nth(i)
        href = anchor.get_attribute('href')
        if href:
            all_hrefs.append(href)

    base_url = "https://bd.infinixmobility.com/specs"
    final_links = [base_url + href for href in all_hrefs]

    print("\n--- All Product Links ---")
    for i, link in enumerate(final_links):
        print(f"{i+1}: {link}")
    print("-------------------------\n")

    for link in final_links:
        print(f"Visiting: {link}")
        page.goto(link, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)
