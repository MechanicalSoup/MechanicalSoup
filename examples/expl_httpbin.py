import mechanicalsoup

browser = mechanicalsoup.StatefulBrowser()
browser.open("http://httpbin.org/")

print(browser.get_url())
browser.follow_link("forms")
print(browser.get_url())
print(browser.get_current_page())

browser.select_form('form[action="/post"]')
browser["custname"] = "Me"
browser["custtel"] = "00 00 0001"
browser["custemail"] = "nobody@example.com"
browser["size"] = "medium"
browser["topping"] = "onion"
browser["topping"] = ("bacon", "cheese")

# Uncomment to launch a real web browser on the current page.
# browser.launch_browser()
response = browser.submit_selected()
print(response.text)
