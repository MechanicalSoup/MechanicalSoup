from .utils import LinkNotFoundError
from bs4 import BeautifulSoup


class Form(object):

    def __init__(self, form):
        self.form = form

    def input(self, data):
        """Fill-in a set of fields in a form.

        Example: filling-in a login/password form

        .. code-block:: python

           form.input({"login": username, "password": password})

        This will find the input element named "login" and give it the
        value ``username``, and the input element named "password" and
        give it the value ``password``.

        The type of element (input, textarea, select, ...) does not
        need to be given.
        """

        for (name, value) in data.items():
            i = self.form.find("input", {"name": name})
            if not i:
                raise LinkNotFoundError("No input field named " + name)
            i["value"] = value

    attach = input

    def uncheck_all(self, name):
        for option in self.form.find_all("input", {"name": name}):
            if "checked" in option.attrs:
                del option.attrs["checked"]

    def check(self, data):
        for (name, value) in data.items():
            # Complain if we don't find the name, regardless of the
            # value
            inputs = self.form.find_all("input", {"name": name})
            if inputs == []:
                raise LinkNotFoundError("No input checkbox named " + name)
            type = inputs[0].attrs.get('type', 'text')
            if type == "radio":
                self.uncheck_all(name)

            # Accept individual values (int, str)
            # We just wrap them in a 1-value tuple.
            if not isinstance(value, list) and not isinstance(value, tuple):
                value = (value,)
            for choice in value:
                choice = str(choice)  # Allow for example literal numbers
                found = False
                for i in inputs:
                    if i.attrs.get("value", "on") == choice:
                        i["checked"] = ""
                        found = True
                        break
                if not found:
                    print(self.form)
                    raise LinkNotFoundError(
                        "No input checkbox named %s with choice %s" %
                        (name, choice)
                    )

    def textarea(self, data):
        for (name, value) in data.items():
            t = self.form.find("textarea", {"name": name})
            if not t:
                raise LinkNotFoundError("No textarea named " + name)
            t.string = value

    def __setitem__(self, name, value):
        return self.set(name, value)

    def set(self, name, value, force=False):
        input = self.form.find("input", {"name": name})
        if input:
            if input.attrs.get('type', 'text') in ("radio", "checkbox"):
                if value is True:
                    # f["foo"] = True checks the box foo
                    input.attrs["checked"] = ""
                elif value is False:
                    # f["foo"] = False unchecks it
                    del input.attrs["checked"]
                else:
                    self.check({name: value})
            else:
                input["value"] = value
            return
        textarea = self.form.find("textarea", {"name": name})
        if textarea:
            textarea.string = value
            return
        select = self.form.find("select", {"name": name})
        if select:
            for option in select.find_all("option"):
                if "selected" in option.attrs:
                    del option.attrs["selected"]
            o = select.find("option", {"value": value})
            o.attrs["selected"] = "selected"
            return
        if force:
            self.new_control('input', name, value=value)
            return
        raise LinkNotFoundError()

    def new_control(self, type, name, value, **kwargs):
        old = self.form.find('input', {'name': name})
        if old:
            old.decompose()
        old = self.form.find('textarea', {'name': name})
        if old:
            old.decompose()
        # We don't have access to the original soup object, so we
        # instantiate a new BeautifulSoup() to call new_tag().
        control = BeautifulSoup().new_tag('input')
        control['type'] = type
        control['name'] = name
        control['value'] = value
        for k, v in kwargs.items():
            control[k] = v
        self.form.append(control)
        return control

    def choose_submit(self, el):
        '''Selects the submit input (or button) element specified by 'el',
        where 'el' can be either a bs4.element.Tag or just its name attribute.
        If the element is not found or if multiple elements match, raise a
        LinkNotFoundError exception.'''
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

        found = False
        inps = self.form.select('input[type="submit"], button[type="submit"]')
        for inp in inps:
            if inp == el or inp['name'] == el:
                if found:
                    raise LinkNotFoundError(
                        "Multiple submit elements match: {0}".format(el)
                    )
                found = True
                continue

            del inp['name']

        if not found:
            raise LinkNotFoundError(
                "Specified submit element not found: {0}".format(el)
            )
