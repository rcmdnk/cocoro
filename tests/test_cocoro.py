import pytest
from cocoro import __version__
from cocoro import Cocoro


@pytest.fixture(scope='module')
def co():
    return Cocoro(config_file='./tests/data/config.yml')


def test_version():
    assert __version__ == '0.1.4'


def test_cocoro(co):
    assert co.config['appSecret'] == 'abc%3Ddef'
    assert co.config['terminalAppIdKey'] == 'abcd'
