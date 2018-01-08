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
    browser, mock = prepare_mock_browser()
    mock_get(mock, url, text)

    if expected_post is not None:
        mock_post(mock, url + '/post', expected_post)

    return browser, url


def prepare_mock_browser(scheme='mock'):
    mock = requests_mock.Adapter()
    browser = mechanicalsoup.StatefulBrowser(requests_adapters={scheme: mock})

    return browser, mock


def mock_get(mocked_adapter, url, reply, content_type='text/html'):
    headers = {'Content-Type': content_type}
    mocked_adapter.register_uri('GET', url, headers=headers, text=reply)


def mock_post(mocked_adapter, url, expected, reply='Success!'):
    def text_callback(request, context):
        # Python 2's parse_qsl doesn't like None argument
        query = parse_qsl(request.text) if request.text else ()
        assert (set(query) == set(expected))
        return reply

    mocked_adapter.register_uri('POST', url, text=text_callback)


class HttpbinRemote:
    """Drop-in replacement for pytest-httpbin's httpbin fixture
    that uses the remote httpbin server instead of a local one."""
    def __init__(self):
        self.url = "http://httpbin.org"

    def __add__(self, x):
        return self.url + x
