import logging
import pytest
from cocoro import __version__
from cocoro import Cocoro


@pytest.fixture(scope='module', name='my_cocoro')
def fixture_cocoro():
    return Cocoro(config_file='./tests/data/config.yml')


def test_version():
    assert __version__ == '0.1.4'


def test_read_config(my_cocoro):
    assert my_cocoro.config['appSecret'] == 'abc%3Ddef'
    assert my_cocoro.config['terminalAppIdKey'] == 'abcd'


def test_cocoro(my_cocoro):
    assert my_cocoro.config['appSecret'] == 'abc%3Ddef'
    assert my_cocoro.config['terminalAppIdKey'] == 'abcd'


params = {'int': (1, 1), 'str_int': ('1', 1),
          'info': ('info', logging.INFO), 'invalid': ('invalid', -1)}


@pytest.mark.parametrize('log_level, result',
                         list(params.values()), ids=list(params.keys()))
def test_get_log_level(my_cocoro, log_level, result):
    assert my_cocoro.get_log_level(log_level) == result
