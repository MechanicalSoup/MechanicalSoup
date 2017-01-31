from .utils import LinkNotFoundError


class Form(object):

    def __init__(self, form):
        self.form = form

    def input(self, data):
        for (name, value) in data.items():
            i = self.form.find("input", {"name": name})
            if not i:
                raise LinkNotFoundError("No input field named " + name)
            i["value"] = value

    attach = input

    def check(self, data):
        for (name, value) in data.items():
            if not isinstance(value, list):
                value = (value,)
            for choice in value:
                i = self.form.find("input", {"name": name, "value": choice})
                if not i:
                    raise LinkNotFoundError("No input checkbox named " + name)
                i["checked"] = ""

    def textarea(self, data):
        for (name, value) in data.items():
            t = self.form.find("textarea", {"name": name})
            if not t:
                raise LinkNotFoundError("No textarea named " + name)
            t.string = value

    def choose_submit(self, el):
        # In a normal web browser, when a input[type=submit] is clicked,
        # all other submits aren't sent. You can use simulate this as
        # following:

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
