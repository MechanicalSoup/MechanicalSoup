import pytest

# This file is automatically discovered by pytest to define
# shared fixtures only once.


@pytest.fixture
def httpbin():
    from utils import HttpbinRemote
    return HttpbinRemote()
