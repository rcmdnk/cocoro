import logging
import fire
from .__init__ import __version__, __program__
from .core import Cocoro


class CliObject:
    '''Utilities to use Sharp, COCORO API'''

    def __init__(self):
        pass

    @staticmethod
    def version():
        '''Show version'''
        print("%s: %s" % (__program__, __version__))

    @staticmethod
    def switch(*args, **kw):
        '''Control switch (on/off)'''
        Cocoro(**kw).device_control('switch', args[0])

    @staticmethod
    def humidification(*args, **kw):
        '''Control humidification (on/off)'''
        Cocoro(**kw).device_control('humi', args[0])

    @staticmethod
    def humi(*args, **kw):
        '''Control humidification (on/off)'''
        Cocoro(**kw).device_control('humi', args[0])

    @staticmethod
    def mode(*args, **kw):
        '''Control mode
        (auto/sleep/pollen/quiet/medium/high/recommendation/effective)'''
        Cocoro(**kw).device_control('mode', args[0])


def cli():
    logging.basicConfig(handlers=[logging.StreamHandler()],
                        format='[%(levelname)s][%(name)s] %(message)s')
    fire.Fire(CliObject)
