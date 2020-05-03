"""WARNING: this script does not seem to work with the current
DuckDuckGo version (as of 2019/08).

Example usage of MechanicalSoup to get the results from
DuckDuckGo.
"""

import mechanicalsoup

# Connect to duckduckgo
browser = mechanicalsoup.StatefulBrowser(user_agent="MechanicalSoup")

# Go to url
browser.open("https://duckduckgo.com")

# Add value to input box
browser.get_current_page().find("input").attrs["value"] = "MechanicalSoup"

# find submit button
submit = browser.get_current_page().find("input", id="search_button_homepage")
form = browser.select_form()

form.choose_submit(submit)

browser.submit_selected()


# Display the results
for link in browser.links():
    print(link.text, "->", link.attrs["href"])

