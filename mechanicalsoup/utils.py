class LinkNotFoundError(Exception):
    """Exception raised when mechanicalsoup fails to find something.

    This happens in situations like (non-exhaustive list):

    * :func:`~mechanicalsoup.StatefulBrowser.find_link` is called, but
      no link is found.

    * The browser was configured with raise_on_404=True and a 404
      error is triggered while browsing.

    * The user tried to fill-in a field which doesn't exist in a form
      (e.g. browser["name"] = "val" with browser being a
      StatefulBrowser).
    """
    pass


def is_multipart_file_upload(form, tag):
    return (
        form.get("enctype", "") == "multipart/form-data" and
        tag.get("type", "").lower() == "file"
    )


def is_disabled(tag):
    """Return whether a form control is disabled per the HTML specification.

    A control is disabled if it carries a ``disabled`` attribute, or if it is
    a descendant of a ``<fieldset>`` element whose ``disabled`` attribute is
    set -- except when it is inside that fieldset's first ``<legend>`` child,
    which stays enabled. Disabled controls are barred from submission, so
    browsers do not include their name/value pairs in the form data.

    https://html.spec.whatwg.org/multipage/form-elements.html#concept-fieldset-disabled
    """
    if tag.has_attr("disabled"):
        return True
    for fieldset in tag.find_parents("fieldset"):
        if not fieldset.has_attr("disabled"):
            continue
        # Controls inside the disabled fieldset's first <legend> child are
        # not disabled by that fieldset.
        legend = fieldset.find("legend", recursive=False)
        if legend is not None and any(p is legend for p in tag.parents):
            continue
        return True
    return False
