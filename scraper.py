import re
from playwright.sync_api import sync_playwright

def run():
    total_grand_sum = 0
    seeds = range(82, 92)  # Seeds 82 to 91
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for seed in seeds:
            url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
            print(f"Scraping {url}...")
            
            try:
                page.goto(url, wait_until="networkidle")
                # Wait for the JavaScript to actually build the table
                page.wait_for_selector("td", timeout=10000)
                
                # Get all table cell values
                cells = page.locator("td").all_inner_texts()
                
                seed_sum = 0
                for text in cells:
                    # Remove anything that isn't a digit, dot, or minus sign
                    clean_val = re.sub(r'[^\d.-]', '', text)
                    if clean_val:
                        try:
                            seed_sum += float(clean_val)
                        except ValueError:
                            continue
                
                print(f"Subtotal for Seed {seed}: {seed_sum}")
                total_grand_sum += seed_sum
            except Exception as e:
                print(f"Error on seed {seed}: {e}")
                
        browser.close()
    
    print("\n" + "="*40)
    print(f"FINAL TOTAL SUM: {total_grand_sum}")
    print("="*40)

if __name__ == "__main__":
    run()
