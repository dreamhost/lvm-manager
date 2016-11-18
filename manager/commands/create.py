import logging

from cliff.lister import Lister

from manager.utils.common import lv_path, lv_create, pv_create, vg_create, xfs_format


class Create(Lister):

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)
        parser.add_argument('vg')
        parser.add_argument('device')
        return parser

    def take_action(self, parsed_args):
        vg_name = parsed_args.vg
        device = parsed_args.device
        path = None
        try:
            pv_create(device)
            vg_create(vg_name, [device])
            lv_create(vg_name, 'home')
            path = lv_path(vg_name, 'home')
            xfs_format(path)
        except Exception as e:
            raise "Failed to create %s with device %s\n%s" % (vg_name,
                                                              device,
                                                              e)

        return [
            ('device', 'vg', 'path', 'result'),
            [(device, vg_name, path, 'pass')]
        ]
