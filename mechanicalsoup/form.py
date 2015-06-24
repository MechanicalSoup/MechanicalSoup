class Form:

    def __init__(self, form):
        self.form = form

    def input(self, data):
        for (name, value) in data.items():
            self.form.find("input", {"name": name})["value"] = value

    def check(self, data):
        for (name, value) in data.items():
            self.form.find("input", {"name": name, "value": value})[
                "checked"] = ""

    def textarea(self, data):
        for (name, value) in data.items():
            self.form.find("textarea", {"name": name}).insert(0, value)

    def attach(self, data):
        for (name, value) in data.items():
            self.form.find("input", {"name": name})["value"] = value
