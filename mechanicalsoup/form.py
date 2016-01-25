class Form(object):

    def __init__(self, form):
        self.form = form

    def input(self, data):
        for (name, value) in data.items():
            self.form.find("input", {"name": name})["value"] = value

    def check(self, data):
        for (name, value) in data.items():
            if isinstance(value, list):
                for choice in value:
                    self.form.find("input", {"name": name, "value": choice})[
                        "checked"] = ""
            else:
                self.form.find("input", {"name": name, "value": value})[
                    "checked"] = ""

    def textarea(self, data):
        for (name, value) in data.items():
            self.form.find("textarea", {"name": name}).insert(0, value)

    def attach(self, data):
        for (name, value) in data.items():
            self.form.find("input", {"name": name})["value"] = value

    def choose_submit(self, el):
        # In a normal web browser, when a input[type=submit] is clicked,
        # all other submits aren't sent. You can use simulate this as following:

        # page = browser.get(URL)
        # form_el = page.soup.form
        # form = Form(form_el)
        # submit = page.soup.select(SUBMIT_SELECTOR)[0]
        # form.choose_submit(submit)
        # url = BASE_DOMAIN + form_el.attrs['action']
        # return browser.submit(form, url)

        for inp in self.form.select("input"):
            if inp.get('type') != 'submit':
                continue
            if inp == el:
                continue

            del inp['name']
            return True

        return False
