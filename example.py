"""Example app to login to GitHub"""
import argparse
import mechanicalsoup

parser = argparse.ArgumentParser(description='Login to GitHub.')
parser.add_argument("username")
parser.add_argument("password")
args = parser.parse_args()

browser = mechanicalsoup.Browser()

# request github login page
login_page = browser.get("https://github.com/login")

# find login form
login_form = login_page.soup.select("#login")[0].select("form")[0]

# specify username and password
login_form.select("#login_field")[0]['value'] = args.username
login_form.select("#password")[0]['value'] = args.password

# submit!
page2 = browser.submit(login_form, login_page.response.url)

# verify we are now logged in
assert page2.soup.select(".logout-form")

# verify we remain logged in (thanks to cookies) as we browse the rest of the site
page3 = browser.get("https://github.com/matt-hickford/MechanicalSoup")
assert page3.soup.select(".logout-form")
