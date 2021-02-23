import fire
from .__init__ import __version__, __program__
from .core import Cocoro


class CliObject(object):
    '''Utilities to use Sharp, COCORO API'''

    def __init__(self):
        pass

    def version(self):
        '''Show version'''
        print("%s: %s" % (__program__, __version__))

    def on(self, **kw):
        '''Switch on'''
        Cocoro(**kw).on()

    def off(self, **kw):
        '''Switch off'''
        Cocoro(**kw).off()

    def humi_on(self, **kw):
        '''Humidification on'''
        Cocoro(**kw).humi_on()

    def humi_off(self, **kw):
        '''Humidification off'''
        Cocoro(**kw).humi_off()

    def mode_auto(self, **kw):
        '''Set mode: Auto'''
        Cocoro(**kw).mode_auto()

    def mode_sleep(self, **kw):
        '''Set mode: Sleep'''
        Cocoro(**kw).mode_sleep()

    def mode_pollen(self, **kw):
        '''Set mode: Pollen'''
        Cocoro(**kw).mode_pollen()

    def mode_quiet(self, **kw):
        '''Set mode: Quiet'''
        Cocoro(**kw).mode_quiet()

    def mode_medium(self, **kw):
        '''Set mode: Medium'''
        Cocoro(**kw).mode_medium()

    def mode_high(self, **kw):
        '''Set mode: High'''
        Cocoro(**kw).mode_high()

    def mode_recommendation(self, **kw):
        '''Set mode: Recommendation'''
        Cocoro(**kw).mode_recommendation()

    def mode_effective(self, **kw):
        '''Set mode: Effective'''
        Cocoro(**kw).mode_effective()


def cli():
    fire.Fire(CliObject)
