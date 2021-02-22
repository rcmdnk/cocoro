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

    def box(self, **kw):
        Cocoro(**kw).box()


def cli():
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help', 'help']:
        print("%s: %s" % (__program__, 'Usage: cocoro <cmd>'))
    else:
        fire.Fire(CliObject)
