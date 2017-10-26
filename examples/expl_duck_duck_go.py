"""Example usage of MechanicalSoup to get the results from
DuckDuckGo."""

import mechanicalsoup

# Connect to duckduckgo
browser = mechanicalsoup.StatefulBrowser()
browser.open("https://duckduckgo.com/")

# Fill-in the search form
browser.select_form('#search_form_homepage')
browser["q"] = "MechanicalSoup"
browser.submit_selected()

# Display the results
for link in browser.get_current_page().select('a.result__a'):
    print(link.text, '->', link.attrs['href'])
