"""WARNING: this script does not seem to work with the current
DuckDuckGo version (as of 2019/08).

Example usage of MechanicalSoup to get the results from
DuckDuckGo.
"""

import mechanicalsoup

# Connect to duckduckgo
browser = mechanicalsoup.StatefulBrowser()
browser.open("https://duckduckgo.com/")

# Fill-in the search form
browser.select_form('#search_form_input_homepage')
browser["q"] = "MechanicalSoup"
browser.submit_selected()

# Display the results
for link in browser.page.select('a.result__a'):
    print(link.text, '->', link.attrs['href'])
