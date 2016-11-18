import logging
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager


class LvmManager(App):

    log = logging.getLogger(__name__)
    keystone = None

    def __init__(self, stdout=None, auth={}):
        super(LvmManager, self).__init__(
            description='Management tool for LVM',
            version='0.1',
            command_manager=CommandManager('manager'),
            stdout=stdout
        )

#    def initialize_app(self, argv):
#        print "initialize"

    def build_option_parser(self, *args, **kwargs):
        parser = super(LvmManager, self).build_option_parser(*args, **kwargs)
        return parser


def main(argv=sys.argv[1:]):
    l = LvmManager()
    return l.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
