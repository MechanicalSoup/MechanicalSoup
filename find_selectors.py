from playwright.sync_api import sync_playwright

def find_selectors():
    """
    Interactive script to find selectors for desired elements.
    """
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)  # Run in non-headless mode for interaction
        page = browser.new_page()

        try:
            # Navigate to the URL
            page.goto("https://whop.com/discover/f/most_affiliate_earnings_24_hours/")

            print("Click on the elements you want to scrape. The script will log their selectors.")

            # Set up a loop to listen for clicks and log selectors
            while True:
                # Wait for the user to click an element
                print("Click on an element to get its selector (or press Ctrl+C to exit)...")
                try:
                    # Wait for a click event
                    page.wait_for_event("click", timeout=0)
                except KeyboardInterrupt:
                    print("Exiting...")
                    break

                # Get the last clicked element
                clicked_element = page.evaluate("""() => {
                    return window.lastClickedElement;
                }""")

                if clicked_element:
                    # Log the selector for the clicked element
                    selector = page.evaluate("""(element) => {
                        // Generate a unique selector for the element
                        function getSelector(el) {
                            if (!el) return null;
                            const path = [];
                            while (el.nodeType === Node.ELEMENT_NODE) {
                                let selector = el.nodeName.toLowerCase();
                                if (el.id) {
                                    selector += `#${el.id}`;
                                    path.unshift(selector);
                                    break;
                                } else {
                                    let sibling = el;
                                    let nth = 1;
                                    while (sibling.previousElementSibling) {
                                        sibling = sibling.previousElementSibling;
                                        nth++;
                                    }
                                    if (nth !== 1) selector += `:nth-of-type(${nth})`;
                                }
                                path.unshift(selector);
                                el = el.parentNode;
                            }
                            return path.join(' > ');
                        }
                        return getSelector(element);
                    }""", clicked_element)

                    print(f"Selector for the clicked element: {selector}")

        except Exception as e:
            print(f"Error during execution: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    find_selectors()