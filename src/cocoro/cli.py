import sys
import logging
import fire
from .__init__ import __version__, __program__
from .core import Cocoro


class CliObject:
    '''Utilities to use Sharp, COCORO API'''

    def __init__(self):
        pass

    @staticmethod
    def run(ret=True):
        if ret:
            sys.exit(0)
        else:
            sys.exit(1)

    def version(self):
        '''Show version'''
        print("%s: %s" % (__program__, __version__))
        self.run()

    def switch(self, *args, **kw):
        '''Control switch (on/off)'''
        self.run(Cocoro(**kw).device_control('switch', args[0]))

    def humidification(self, *args, **kw):
        '''Control humidification (on/off)'''
        self.run(Cocoro(**kw).device_control('humidification', args[0]))

    def humi(self, *args, **kw):
        '''Control humidification (on/off)'''
        self.run(self.humidification(*args, **kw))

    def mode(self, *args, **kw):
        '''Control mode
        (auto/sleep/pollen/quiet/medium/high/recommendation/effective)'''
        self.run(Cocoro(**kw).device_control('mode', args[0]))

    def info(self, *arg, **kw):
        '''Show device information'''
        info = Cocoro(**kw).devince_info(*arg)
        if not info:
            sys.exit(1)
        print(info)
        self.run()


def cli():
    logging.basicConfig(handlers=[logging.StreamHandler()],
                        format='[%(levelname)s][%(name)s] %(message)s')
    fire.Fire(CliObject)
