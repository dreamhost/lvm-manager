import logging
import subprocess

import lvm

log = logging.getLogger(__name__)


def vg_exists(vg_name):
    vg = None
    try:
        vg = lvm.vgOpen(vg_name, 'r')
    except Exception as e:
#        log.debug(e)
        return False

    return vg


def pv_create(device):
    return lvm.pvCreate(device)


def vg_create(vg_name, devices=[]):
    """
    creates a volume group in LVM
    """

    if vg_exists(vg_name):
        return True

    log.info("Creating VG %s" % vg_name)
    vg = lvm.vgCreate(vg_name)

    for d in devices:
        vg.extend(d)

    vg.close()

    return vg


def lv_exists(vg_name, lv_name):
    if not vg_exists(vg_name):
        return False

    vg = lvm.vgOpen(vg_name, 'r')
    for lv in vg.listLVs():
        if lv.getName() == lv_name:
            return True


def lv_path(vg_name, lv_name):
    if lv_exists(vg_name, lv_name):
        vg = lvm.vgOpen(vg_name, 'r')
        for lv in vg.listLVs():
            if lv.getName() == lv_name:
                lv_path = lv.getProperty('lv_path')
                return lv_path[0]


def lv_create(vg_name, lv_name):
    """
    create lvm
    """
    if lv_exists(vg_name, lv_name):
        log.exception("logical volume %s already exists" % lv_name)

    try:
        cmd = ['lvcreate', '-l', '100%FREE', '-n', vg_name, lv_name]
        subprocess.check_output(cmd)
    except Exception as err:
        log.exception("Failed to lvcreate %s %s : %s" % (vg_name,
                      lv_name, err))
        return False


def xfs_format(path):
    """
    format logical volume
    """

    try:
        cmd = ['mkfs.xfs', path]
        subprocess.check_output(cmd)
    except Exception as err:
        log.exception("Failed to mkfs.xfs %s : %s" % (path, err))


def lv_extend(vg_name, lv_name, size="+100%FREE"):
    """
    Extend existing logical volume
    """

    if lv_exists(vg_name, lv_name):
        lv_device = lv_path(vg_name, lv_name)
        try:
            cmd = ['lvextend', '--resizefs', '-l', size, lv_device]
            subprocess.check_output(cmd)
        except Exception as err:
            log.exception("Failed to lvcreate %s %s : %s" % (vg_name,
                          lv_name, err))
            return False


def pv_get_free_devices():
    rc = []
    with lvm.listPvs() as pvs:
        for p in pvs:
            rc.append(p.getName())
    return rc


def vg_extend(vg_name, devices=[]):
    try:
        vg = lvm.vgOpen(vg_name, 'w')
        for d in devices:
            if in_vg(vg_name, d):
                continue
            else:
                # TODO(jordan) this fails with a locking error, so for now just
                # fork the subprocess. Fix this to work with the lvm module
                # vg.extend(d)


                try:
                    cmd = ['vgextend', vg_name, d]
                    subprocess.check_output(cmd)
                except Exception as err:
                    log.exception("Failed to extend %s %s : %s" % (vg_name,
                                  d, err))

        vg.close()
    except Exception as err:
        print err
#        log.exception(err)


def get_pv(vg):
    pv_list = vg.listPVs()
    return pv_list


def in_vg(vg_name, device):
    vg = lvm.vgOpen(vg_name, 'r')
    pv_list = vg.listPVs()
    for pv in pv_list:
        if pv.getName() == device:
            return True
    return False
