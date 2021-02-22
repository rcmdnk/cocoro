import sys
import fire
from .__init__ import __version__, __program__
from .core import Cocoro


class CliObject(object):

    def __init__(self):
        pass

    def version(self):
        print("%s: %s" % (__program__, __version__))

    def on(self, **kw):
        Cocoro(**kw).on()

    def off(self, **kw):
        Cocoro(**kw).off()

    def humi_on(self, **kw):
        Cocoro(**kw).humi_on()

    def humi_off(self, **kw):
        Cocoro(**kw).humi_off()

    def mode_auto(self, **kw):
        Cocoro(**kw).mode_auto()

    def mode_sleep(self, **kw):
        Cocoro(**kw).mode_sleep()

    def mode_pollen(self, **kw):
        Cocoro(**kw).mode_pollen()

    def mode_quiet(self, **kw):
        Cocoro(**kw).mode_quiet()

    def mode_medium(self, **kw):
        Cocoro(**kw).mode_medium()

    def mode_high(self, **kw):
        Cocoro(**kw).mode_high()

    def mode_recommendation(self, **kw):
        Cocoro(**kw).mode_recommendation()

    def mode_effective(self, **kw):
        Cocoro(**kw).mode_effective()


def cli():
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help', 'help']:
        print("%s: %s" % (__program__, 'Usage: cocoro <cmd>'))
    else:
        fire.Fire(CliObject)
