import re

import mechanicalsoup

# Connect to Google
browser = mechanicalsoup.StatefulBrowser()
browser.open("https://www.google.com/")

# Fill-in the form
browser.select_form('form[action="/search"]')
browser["q"] = "MechanicalSoup"
# Note: the button name is btnK in the content served to actual
# browsers, but btnG for bots.
browser.submit_selected(btnName="btnG")

# Display links
for link in browser.links():
    target = link.attrs['href']
    # Filter-out unrelated links and extract actual URL from Google's
    # click-tracking.
    if (target.startswith('/url?') and not
            target.startswith("/url?q=http://webcache.googleusercontent.com")):
        target = re.sub(r"^/url\?q=([^&]*)&.*", r"\1", target)
        print(target)
