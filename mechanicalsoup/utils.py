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
