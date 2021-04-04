import copy
import warnings

from bs4 import BeautifulSoup

from .utils import LinkNotFoundError


class InvalidFormMethod(LinkNotFoundError):
    """This exception is raised when a method of :class:`Form` is used
    for an HTML element that is of the wrong type (or is malformed).
    It is caught within :func:`Form.set` to perform element type deduction.

    It is derived from :class:`LinkNotFoundError` so that a single base class
    can be used to catch all exceptions specific to this module.
    """
    pass


class Form:
    """Build a fillable form.

    :param form: A bs4.element.Tag corresponding to an HTML form element.

    The Form class is responsible for preparing HTML forms for submission.
    It handles the following types of elements:
    input (text, checkbox, radio), select, and textarea.

    Each type is set by a method named after the type (e.g.
    :func:`~Form.set_select`), and then there are convenience methods (e.g.
    :func:`~Form.set`) that do type-deduction and set the value using the
    appropriate method.

    It also handles submit-type elements using :func:`~Form.choose_submit`.
    """

    def __init__(self, form):
        if form.name != 'form':
            warnings.warn(
                f"Constructed a Form from a '{form.name}' instead of a 'form' "
                " element. This may be an error in a future version of "
                "MechanicalSoup.", FutureWarning)

        self.form = form
        self._submit_chosen = False

        # Aliases for backwards compatibility
        # (Included specifically in __init__ to suppress them in Sphinx docs)
        self.attach = self.set_input
        self.input = self.set_input
        self.textarea = self.set_textarea

    def set_input(self, data):
        """Fill-in a set of fields in a form.

        Example: filling-in a login/password form

        .. code-block:: python

           form.set_input({"login": username, "password": password})

        This will find the input element named "login" and give it the
        value ``username``, and the input element named "password" and
        give it the value ``password``.
        """

        for (name, value) in data.items():
            i = self.form.find("input", {"name": name})
            if not i:
                raise InvalidFormMethod("No input field named " + name)
            i["value"] = value

    def uncheck_all(self, name):
        """Remove the *checked*-attribute of all input elements with
        a *name*-attribute given by ``name``.
        """
        for option in self.form.find_all("input", {"name": name}):
            if "checked" in option.attrs:
                del option.attrs["checked"]

    def check(self, data):
        """For backwards compatibility, this method handles checkboxes
        and radio buttons in a single call. It will not uncheck any
        checkboxes unless explicitly specified by ``data``, in contrast
        with the default behavior of :func:`~Form.set_checkbox`.
        """
        for (name, value) in data.items():
            try:
                self.set_checkbox({name: value}, uncheck_other_boxes=False)
                continue
            except InvalidFormMethod:
                pass
            try:
                self.set_radio({name: value})
                continue
            except InvalidFormMethod:
                pass
            raise LinkNotFoundError("No input checkbox/radio named " + name)

    def set_checkbox(self, data, uncheck_other_boxes=True):
        """Set the *checked*-attribute of input elements of type "checkbox"
        specified by ``data`` (i.e. check boxes).

        :param data: Dict of ``{name: value, ...}``.
            In the family of checkboxes whose *name*-attribute is ``name``,
            check the box whose *value*-attribute is ``value``. All boxes in
            the family can be checked (unchecked) if ``value`` is True (False).
            To check multiple specific boxes, let ``value`` be a tuple or list.
        :param uncheck_other_boxes: If True (default), before checking any
            boxes specified by ``data``, uncheck the entire checkbox family.
            Consider setting to False if some boxes are checked by default when
            the HTML is served.
        """
        for (name, value) in data.items():
            # Case-insensitive search for type=checkbox
            selector = 'input[type="checkbox" i][name="{}"]'.format(name)
            checkboxes = self.form.select(selector)
            if not checkboxes:
                raise InvalidFormMethod("No input checkbox named " + name)

            # uncheck if requested
            if uncheck_other_boxes:
                self.uncheck_all(name)

            # Wrap individual values (e.g. int, str) in a 1-element tuple.
            if not isinstance(value, list) and not isinstance(value, tuple):
                value = (value,)

            # Check or uncheck one or more boxes
            for choice in value:
                choice_str = str(choice)  # Allow for example literal numbers
                for checkbox in checkboxes:
                    if checkbox.attrs.get("value", "on") == choice_str:
                        checkbox["checked"] = ""
                        break
                    # Allow specifying True or False to check/uncheck
                    elif choice is True:
                        checkbox["checked"] = ""
                        break
                    elif choice is False:
                        if "checked" in checkbox.attrs:
                            del checkbox.attrs["checked"]
                        break
                else:
                    raise LinkNotFoundError(
                        "No input checkbox named %s with choice %s" %
                        (name, choice)
                    )

    def set_radio(self, data):
        """Set the *checked*-attribute of input elements of type "radio"
        specified by ``data`` (i.e. select radio buttons).

        :param data: Dict of ``{name: value, ...}``.
            In the family of radio buttons whose *name*-attribute is ``name``,
            check the radio button whose *value*-attribute is ``value``.
            Only one radio button in the family can be checked.
        """
        for (name, value) in data.items():
            # Case-insensitive search for type=radio
            selector = 'input[type="radio" i][name="{}"]'.format(name)
            radios = self.form.select(selector)
            if not radios:
                raise InvalidFormMethod("No input radio named " + name)

            # only one radio button can be checked
            self.uncheck_all(name)

            # Check the appropriate radio button (value cannot be a list/tuple)
            for radio in radios:
                if radio.attrs.get("value", "on") == str(value):
                    radio["checked"] = ""
                    break
            else:
                raise LinkNotFoundError(
                    f"No input radio named {name} with choice {value}"
                )

    def set_textarea(self, data):
        """Set the *string*-attribute of the first textarea element
        specified by ``data`` (i.e. set the text of a textarea).

        :param data: Dict of ``{name: value, ...}``.
            The textarea whose *name*-attribute is ``name`` will have
            its *string*-attribute set to ``value``.
        """
        for (name, value) in data.items():
            t = self.form.find("textarea", {"name": name})
            if not t:
                raise InvalidFormMethod("No textarea named " + name)
            t.string = value

    def set_select(self, data):
        """Set the *selected*-attribute of the first option element
        specified by ``data`` (i.e. select an option from a dropdown).

        :param data: Dict of ``{name: value, ...}``.
            Find the select element whose *name*-attribute is ``name``.
            Then select from among its children the option element whose
            *value*-attribute is ``value``. If no matching *value*-attribute
            is found, this will search for an option whose text matches
            ``value``. If the select element's *multiple*-attribute is set,
            then ``value`` can be a list or tuple to select multiple options.
        """
        for (name, value) in data.items():
            select = self.form.find("select", {"name": name})
            if not select:
                raise InvalidFormMethod("No select named " + name)

            # Deselect all options first
            for option in select.find_all("option"):
                if "selected" in option.attrs:
                    del option.attrs["selected"]

            # Wrap individual values in a 1-element tuple.
            # If value is a list/tuple, select must be a <select multiple>.
            if not isinstance(value, list) and not isinstance(value, tuple):
                value = (value,)
            elif "multiple" not in select.attrs:
                raise LinkNotFoundError("Cannot select multiple options!")

            for choice in value:
                option = select.find("option", {"value": choice})

                # try to find with text instead of value
                if not option:
                    option = select.find("option", string=choice)

                if not option:
                    raise LinkNotFoundError(
                        f'Option {choice} not found for select {name}'
                    )

                option.attrs["selected"] = "selected"

    def __setitem__(self, name, value):
        """Forwards arguments to :func:`~Form.set`. For example,
        :code:`form["name"] = "value"` calls :code:`form.set("name", "value")`.
        """
        return self.set(name, value)

    def set(self, name, value, force=False):
        """Set a form element identified by ``name`` to a specified ``value``.
        The type of element (input, textarea, select, ...) does not
        need to be given; it is inferred by the following methods:
        :func:`~Form.set_checkbox`,
        :func:`~Form.set_radio`,
        :func:`~Form.set_input`,
        :func:`~Form.set_textarea`,
        :func:`~Form.set_select`.
        If none of these methods find a matching element, then if ``force``
        is True, a new element (``<input type="text" ...>``) will be
        added using :func:`~Form.new_control`.

        Example: filling-in a login/password form with EULA checkbox

        .. code-block:: python

            form.set("login", username)
            form.set("password", password)
            form.set("eula-checkbox", True)

        Example: uploading a file through a ``<input type="file"
        name="tagname">`` field (provide the path to the local file,
        and its content will be uploaded):

        .. code-block:: python

            form.set("tagname", path_to_local_file)

        """
        for func in ("checkbox", "radio", "input", "textarea", "select"):
            try:
                getattr(self, "set_" + func)({name: value})
                return
            except InvalidFormMethod:
                pass
        if force:
            self.new_control('text', name, value=value)
            return
        raise LinkNotFoundError("No valid element named " + name)

    def new_control(self, type, name, value, **kwargs):
        """Add a new input element to the form.

        The arguments set the attributes of the new element.
        """
        # Remove existing input-like elements with the same name
        for tag in ('input', 'textarea', 'select'):
            for old in self.form.find_all(tag, {'name': name}):
                old.decompose()
        # We don't have access to the original soup object (just the
        # Tag), so we instantiate a new BeautifulSoup() to call
        # new_tag(). We're only building the soup object, not parsing
        # anything, so the parser doesn't matter. Specify the one
        # included in Python to avoid having dependency issue.
        control = BeautifulSoup("", "html.parser").new_tag('input')
        control['type'] = type
        control['name'] = name
        control['value'] = value
        for k, v in kwargs.items():
            control[k] = v
        self.form.append(control)
        return control

    def choose_submit(self, submit):
        """Selects the input (or button) element to use for form submission.

        :param submit: The bs4.element.Tag (or just its *name*-attribute) that
            identifies the submit element to use. If ``None``, will choose the
            first valid submit element in the form, if one exists.

        To simulate a normal web browser, only one submit element must be
        sent. Therefore, this does not need to be called if there is only
        one submit element in the form.

        If the element is not found or if multiple elements match, raise a
        :class:`LinkNotFoundError` exception.

        Example: ::

            browser = mechanicalsoup.StatefulBrowser()
            browser.open(url)
            form = browser.select_form()
            form.choose_submit('form_name_attr')
            browser.submit_selected()
        """
        # Since choose_submit is destructive, it doesn't make sense to call
        # this method twice unless no submit is specified.
        if self._submit_chosen:
            if submit is None:
                return
            else:
                raise Exception('Submit already chosen. Cannot change submit!')

        # All buttons NOT of type (button,reset) are valid submits
        # Case-insensitive search for type=submit
        inps = [i for i in self.form.select('input[type="submit" i], button')
                if i.get("type", "").lower() not in ('button', 'reset')]

        # If no submit specified, choose the first one
        if submit is None and inps:
            submit = inps[0]

        found = False
        for inp in inps:
            if (inp.has_attr('name') and inp['name'] == submit):
                if found:
                    raise LinkNotFoundError(
                        f"Multiple submit elements match: {submit}"
                    )
                found = True
            elif inp == submit:
                if found:
                    # Ignore submit element since it is an exact
                    # duplicate of the one we're looking at.
                    del inp['name']
                found = True
            else:
                # Delete any non-matching element's name so that it will be
                # omitted from the submitted form data.
                del inp['name']

        if not found and submit is not None:
            raise LinkNotFoundError(
                f"Specified submit element not found: {submit}"
            )
        self._submit_chosen = True

    def print_summary(self):
        """Print a summary of the form.

        May help finding which fields need to be filled-in.
        """
        for input in self.form.find_all(
                ("input", "textarea", "select", "button")):
            input_copy = copy.copy(input)
            # Text between the opening tag and the closing tag often
            # contains a lot of spaces that we don't want here.
            for subtag in input_copy.find_all() + [input_copy]:
                if subtag.string:
                    subtag.string = subtag.string.strip()
            print(input_copy)
