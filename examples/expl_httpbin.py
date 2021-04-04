import mechanicalsoup


browser = mechanicalsoup.StatefulBrowser()
browser.open("http://httpbin.org/")

print(browser.url)
browser.follow_link("forms")
print(browser.url)
print(browser.page)

browser.select_form('form[action="/post"]')
browser["custname"] = "Me"
browser["custtel"] = "00 00 0001"
browser["custemail"] = "nobody@example.com"
browser["size"] = "medium"
browser["topping"] = "onion"
browser["topping"] = ("bacon", "cheese")
browser["comments"] = "This pizza looks really good :-)"

# Uncomment to launch a real web browser on the current page.
# browser.launch_browser()

# Uncomment to display a summary of the filled-in form
# browser.form.print_summary()

response = browser.submit_selected()
print(response.text)
