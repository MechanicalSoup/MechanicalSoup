import io
from email import policy
from email.parser import BytesParser

import bs4
import pytest
import requests
import setpath  # noqa:F401, must come before 'import mechanicalsoup'

import mechanicalsoup


def upload_form(name='photos[]', multiple=True,
                enctype='multipart/form-data'):
    soup = bs4.BeautifulSoup(
        '<form method="post" action="https://upload.invalid/" enctype="{}">'
        '<input type="file" name="{}" {}></form>'.format(
            enctype, name, 'multiple' if multiple else ''), 'html.parser')
    return mechanicalsoup.Form(soup.form)


def multipart_parts(form, **kwargs):
    request = requests.Request(
        **mechanicalsoup.Browser.get_request_kwargs(
            form.form, **kwargs)).prepare()
    message = BytesParser(policy=policy.default).parsebytes(
        ('Content-Type: ' + request.headers['Content-Type'] +
         '\r\nMIME-Version: 1.0\r\n\r\n').encode() + request.body)
    return [(part.get_param('name', header='content-disposition'),
             part.get_filename(), part.get_payload(decode=True))
            for part in message.iter_parts()]


@pytest.mark.parametrize('name', ['photos[]', 'attachments'])
@pytest.mark.parametrize('collection', [list, tuple])
@pytest.mark.parametrize('setter', ['set_input', 'set', 'item'])
def test_multiple_files(name, collection, setter):
    form = upload_form(name=name)
    with io.BytesIO(b'first\x00payload') as first, \
            io.BytesIO(b'second\xffpayload') as second:
        first.name = 'first.bin'
        second.name = 'second.bin'
        files = collection([first, second])
        if setter == 'set_input':
            form.set_input({name: files})
        elif setter == 'set':
            form.set(name, files)
        else:
            form[name] = files
        assert first.tell() == second.tell() == 0
        assert multipart_parts(form) == [
            (name, 'first.bin', b'first\x00payload'),
            (name, 'second.bin', b'second\xffpayload'),
        ]
        assert not first.closed and not second.closed


@pytest.mark.parametrize('multiple', [True, False])
def test_single_file(multiple):
    form = upload_form(multiple=multiple)
    with io.BytesIO(b'single file') as stream:
        form.set_input({'photos[]': stream})
        assert multipart_parts(form) == [('photos[]', '', b'single file')]
        assert not stream.closed


def test_multiple_files_preserve_other_uploads_and_fields():
    form = upload_form()
    form.new_control('text', 'description', 'holiday')
    with io.BytesIO(b'cover') as cover, io.BytesIO(b'photo') as photo, \
            io.BytesIO(b'extra') as extra:
        form.new_control('file', 'cover', cover)
        form.set_input({'photos[]': [photo]})
        parts = multipart_parts(form, files={'extra': ('extra.bin', extra)})
        assert parts == [
            ('description', None, b'holiday'),
            ('extra', 'extra.bin', b'extra'),
            ('photos[]', '', b'photo'),
            ('cover', '', b'cover'),
        ]


@pytest.mark.parametrize('collection', [list, tuple])
def test_empty_selection(collection):
    form = upload_form()
    form.set_input({'photos[]': collection()})
    assert multipart_parts(form) == [('photos[]', '', b'')]


@pytest.mark.parametrize('multiple', [True, False])
def test_invalid_file_collection(multiple):
    form = upload_form(multiple=multiple)
    with io.BytesIO(b'valid') as stream:
        with pytest.raises(ValueError, match='CVE-2023-34457'):
            form.set_input({'photos[]': [stream, '/private/file']})
        assert stream.tell() == 0


def test_non_multiple_input_rejects_file_collection():
    with io.BytesIO(b'file') as stream:
        with pytest.raises(ValueError):
            upload_form(multiple=False).set_input({'photos[]': [stream]})


def test_multiple_files_without_multipart_submit_only_names():
    form = upload_form(enctype='application/x-www-form-urlencoded')
    with io.BytesIO(b'first') as first, io.BytesIO(b'second') as second:
        first.name = '/local/first.bin'
        second.name = '/local/second.bin'
        form.set_input({'photos[]': [first, second]})
        request = requests.Request(
            **mechanicalsoup.Browser.get_request_kwargs(form.form)).prepare()
        assert request.body == 'photos%5B%5D=first.bin&photos%5B%5D=second.bin'
        assert first.tell() == second.tell() == 0


def test_disabled_multiple_files_are_not_read():
    form = upload_form()
    form.form.input['disabled'] = ''
    with io.BytesIO(b'file') as stream:
        form.set_input({'photos[]': [stream]})
        kwargs = mechanicalsoup.Browser.get_request_kwargs(form.form)
        assert not list(kwargs['files'])
        assert stream.tell() == 0


def test_closed_file_reports_error_at_submission():
    form = upload_form()
    with io.BytesIO(b'file') as stream:
        form.set_input({'photos[]': [stream]})
    with pytest.raises(ValueError):
        multipart_parts(form)


def test_server_prefilled_path_never_reads_local_file(tmp_path):
    secret = tmp_path / 'secret.txt'
    secret.write_bytes(b'private contents')
    form = upload_form()
    form.form.input['value'] = str(secret)
    assert multipart_parts(form) == [('photos[]', 'secret.txt', b'')]


def test_form_files_override_keyword_files_with_the_same_name():
    form = upload_form()
    with io.BytesIO(b'first') as first, io.BytesIO(b'second') as second:
        form.set_input({'photos[]': [first, second]})
        parts = multipart_parts(
            form, files={'photos[]': ('old.bin', b'old')})
        assert parts == [
            ('photos[]', '', b'first'), ('photos[]', '', b'second')]
