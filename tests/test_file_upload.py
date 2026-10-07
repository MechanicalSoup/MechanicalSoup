import io

import bs4
import pytest
import requests
import setpath  # noqa:F401, must come before 'import mechanicalsoup'

import mechanicalsoup


UPLOAD_URL = 'https://upload.invalid/'


def upload_form(enctype='multipart/form-data', value=''):
    soup = bs4.BeautifulSoup(
        '<form method="post" action="{}" enctype="{}">'
        '<input type="file" name="upload" {}></form>'.format(
            UPLOAD_URL, enctype, value), 'html.parser')
    return mechanicalsoup.Form(soup.form)


def set_upload(form, value, route):
    if route == 'set':
        form.set('upload', value)
    elif route == 'set_input':
        form.set_input({'upload': value})
    elif route == 'item':
        form['upload'] = value
    elif route == 'new_control':
        form.new_control('file', 'upload', value)
    else:
        form.form.input['value'] = value


def prepare(form):
    kwargs = mechanicalsoup.Browser.get_request_kwargs(form.form)
    return requests.Request(**kwargs).prepare()


@pytest.mark.parametrize('route', [
    'set', 'set_input', 'item', 'new_control', 'raw_soup',
])
def test_explicit_file_content_type(tmp_path, route):
    path = tmp_path / 'local-name.txt'
    payload = b'\x00binary upload\xff\r\n'
    path.write_bytes(payload)
    form = upload_form()
    with path.open('rb') as stream:
        set_upload(form, (stream, 'application/x-report'), route)
        request = prepare(form)
        assert 'multipart/form-data; boundary=' in request.headers[
            'Content-Type']
        assert b'name="upload"; filename="local-name.txt"' in request.body
        assert b'Content-Type: application/x-report\r\n' in request.body
        assert b'\r\n\r\n' + payload + b'\r\n' in request.body
        assert str(tmp_path).encode() not in request.body
        assert not stream.closed


def test_stateful_explicit_file_content_type(requests_mock):
    html = str(upload_form().form)
    requests_mock.post(UPLOAD_URL, text='accepted')
    with mechanicalsoup.StatefulBrowser(
            soup_config={'features': 'html.parser'}) as browser:
        browser.open_fake_page(html, UPLOAD_URL)
        browser.select_form()
        with io.BytesIO(b'file contents') as stream:
            browser['upload'] = (stream, 'application/x-report')
            response = browser.submit_selected()
            assert response.text == 'accepted'
            body = requests_mock.last_request.body
            assert b'Content-Type: application/x-report\r\n' in body
            assert b'filename=""' in body
            assert b'\r\n\r\nfile contents\r\n' in body
            assert not stream.closed


@pytest.mark.parametrize('route', [
    'set', 'set_input', 'new_control', 'raw_soup',
])
@pytest.mark.parametrize('bad_value', [
    ('/path/to/secret', 'application/pdf'),
    (b'contents', 'application/pdf'),
    (None, 'application/pdf'),
    (io.StringIO('text'), 'text/plain'),
    (io.BytesIO(), ''),
    (io.BytesIO(), None),
    (io.BytesIO(), 'text/plain\r\nX-Injected: yes'),
    (io.BytesIO(), 'text/plain\nX-Injected: yes'),
    (42, 'text/plain'),
    (io.BytesIO(),),
    ('report.bin', io.BytesIO(), 'text/plain'),
])
def test_invalid_file_upload_tuple(route, bad_value):
    form = upload_form()
    with pytest.raises(ValueError):
        set_upload(form, bad_value, route)
        prepare(form)


@pytest.mark.parametrize('route', [
    'set', 'set_input', 'new_control', 'raw_soup',
])
@pytest.mark.parametrize('stream_state', ['closed', 'write_only'])
def test_unreadable_file_upload_tuple(tmp_path, route, stream_state):
    path = tmp_path / 'file.bin'
    with path.open('wb') as stream:
        if stream_state == 'closed':
            stream.close()
        form = upload_form()
        with pytest.raises(ValueError):
            set_upload(form, (stream, 'application/octet-stream'), route)
            prepare(form)


def test_file_object_upload_unchanged(tmp_path):
    path = tmp_path / 'report.bin'
    path.write_bytes(b'old upload API')
    form = upload_form()
    with path.open('rb') as stream:
        form['upload'] = stream
        kwargs = mechanicalsoup.Browser.get_request_kwargs(form.form)
        assert kwargs['files']['upload'] == ('report.bin', stream)
        request = requests.Request(**kwargs).prepare()
        assert b'old upload API' in request.body
        assert b'filename="report.bin"' in request.body
        assert b'Content-Type:' not in request.body
        assert not stream.closed


def test_empty_file_upload_unchanged():
    request = prepare(upload_form())
    assert b'name="upload"; filename=""' in request.body
    assert b'Content-Type:' not in request.body


@pytest.mark.parametrize('route', ['set', 'set_input', 'item', 'new_control'])
def test_file_path_rejected(tmp_path, route):
    path = tmp_path / 'secret.txt'
    path.write_bytes(b'PRIVATE CONTENTS')
    with pytest.raises(ValueError, match='CVE-2023-34457'):
        set_upload(upload_form(), str(path), route)


def test_server_prefilled_file_path_never_read(tmp_path):
    path = tmp_path / 'secret.txt'
    path.write_bytes(b'PRIVATE CONTENTS')
    form = upload_form(value='value="{}"'.format(path))
    kwargs = mechanicalsoup.Browser.get_request_kwargs(form.form)
    assert kwargs['files']['upload'] == ('secret.txt', '')
    request = requests.Request(**kwargs).prepare()
    assert b'PRIVATE CONTENTS' not in request.body
    assert b'filename="secret.txt"' in request.body


@pytest.mark.parametrize('enctype', ['', 'application/x-www-form-urlencoded'])
@pytest.mark.parametrize('named', [True, False])
def test_file_tuple_without_multipart(tmp_path, enctype, named):
    path = tmp_path / 'report.bin'
    path.write_bytes(b'PRIVATE CONTENTS')
    stream = path.open('rb') if named else io.BytesIO(b'PRIVATE CONTENTS')
    with stream:
        form = upload_form(enctype=enctype)
        form['upload'] = (stream, 'application/octet-stream')
        request = prepare(form)
        assert request.body == ('upload=report.bin' if named else 'upload=')
        assert stream.tell() == 0


def test_disabled_file_tuple_not_read():
    with io.BytesIO(b'PRIVATE CONTENTS') as stream:
        form = upload_form()
        form.form.input['disabled'] = ''
        form['upload'] = (stream, 'application/octet-stream')
        kwargs = mechanicalsoup.Browser.get_request_kwargs(form.form)
        assert kwargs['files'] == {}
        assert stream.tell() == 0


def test_file_tuple_closed_before_submission():
    form = upload_form()
    with io.BytesIO(b'contents') as stream:
        form['upload'] = (stream, 'application/octet-stream')
    with pytest.raises(ValueError):
        prepare(form)


def test_existing_text_stream_upload_unchanged():
    with io.StringIO('old text stream API') as stream:
        form = upload_form()
        form['upload'] = stream
        request = prepare(form)
        assert b'old text stream API' in request.body
        assert not stream.closed


def test_file_tuple_preserves_other_controls():
    with io.BytesIO(b'file contents') as stream:
        form = upload_form()
        form.new_control('text', 'description', 'normal form field')
        form['upload'] = (stream, 'application/octet-stream')
        request = prepare(form)
        assert b'name="description"\r\n\r\nnormal form field' in request.body
        assert b'\r\n\r\nfile contents\r\n' in request.body


def test_tuple_stream_filename_is_not_opened(tmp_path):
    path = tmp_path / 'secret.txt'
    path.write_bytes(b'PRIVATE CONTENTS')
    with io.BytesIO(b'explicitly supplied contents') as stream:
        form = upload_form()
        stream.name = str(path)
        form['upload'] = (stream, 'application/octet-stream')
        request = prepare(form)
        assert b'PRIVATE CONTENTS' not in request.body
        assert b'explicitly supplied contents' in request.body
