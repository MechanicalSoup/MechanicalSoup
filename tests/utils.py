import mechanicalsoup
import requests_mock
try:
    from urllib.parse import parse_qsl
except ImportError:
    from urlparse import parse_qsl

"""
Utilities for testing MechanicalSoup.
"""

choose_submit_form = '''
<html>
  <body>
    <!-- vaguely based on Trac edit-page form -->
    <form id="choose-submit-form" method="post" action="mock://form.com/post">
      <textarea id="text" class="wikitext trac-resizable" name="text"
        cols="80" rows="40">
      </textarea>
      <div class="field">
        <label>Comment about this change (optional):<br />
          <input id="comment" type="text" name="comment" size="80" value="" />
        </label>
      </div>
      <div class="buttons">
        <input type="submit" name="preview" value="Preview Page" />
        <input type="submit" name="diff" value="Review Changes" />
        <input type="submit" id="save" name="save" value="Submit changes" />
        <button type="submit" name="cancel" value="Cancel" />
      </div>
    </form>
  </body>
</html>
'''


def setup_mock_browser(expected_post=None, text=choose_submit_form):
    url = 'mock://form.com'
    mock = requests_mock.Adapter()
    mock.register_uri('GET', url, headers={'Content-Type': 'text/html'},
                      text=text)

    if expected_post is not None:
        def text_callback(request, context):
            # Python 2's parse_qsl doesn't like None argument
            query = parse_qsl(request.text) if request.text else ()
            assert list(query) == list(expected_post)
            return 'Success!'
        mock.register_uri('POST', url + '/post', text=text_callback)

    browser = mechanicalsoup.StatefulBrowser(requests_adapters={'mock': mock})
    return browser, url


class HttpbinRemote:
    """Drop-in replacement for pytest-httpbin's httpbin fixture
    that uses the remote httpbin server instead of a local one."""
    def __init__(self):
        self.url = "http://httpbin.org"

    def __add__(self, x):
        return self.url + x
