import pytest

import mechanicalsoup


def test_LinkNotFoundError():
    with pytest.raises(mechanicalsoup.LinkNotFoundError):
        raise mechanicalsoup.utils.LinkNotFoundError
    with pytest.raises(Exception):
        raise mechanicalsoup.utils.LinkNotFoundError
