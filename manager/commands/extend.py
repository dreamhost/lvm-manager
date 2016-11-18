import logging

from cliff.lister import Lister
from manager.utils.common import lv_extend, pv_create, vg_extend


class Extend(Lister):

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Extend, self).get_parser(prog_name)
        parser.add_argument('vg')
        parser.add_argument('device')
        return parser

    def take_action(self, parsed_args):
        vg_name = parsed_args.vg
        device = parsed_args.device
        pv_create(device)
        vg_extend(vg_name, [device])
        lv_extend(vg_name, 'home')

        return [
            ('device', 'vg', 'result'),
            [(device, vg_name, 'pass')]
        ]
