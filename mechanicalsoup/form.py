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
