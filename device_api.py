import os
import pathlib
import subprocess
import sys

from ResultModel import ResultModel

script_afhba404_get_ident = 'AFHBA404/scripts/afhba404-get-ident'
script_load_nirq = 'AFHBA404/scripts/loadNIRQ'
script_mount_ramdisk = 'AFHBA404/scripts/mount-ramdisk'
script_get_ident_all = 'AFHBA404/scripts/get-ident-all'
script_ping_acq2106_176 = 'ping -c 4 acq2106_176'

path = '/usr/local/large_dram_data_capture_fat/driver'
acq2106_hts_path = './user_apps/acq2106/acq2106_hts.py'
exec_path = ''

if getattr(sys, 'frozen', False):
    exec_path = os.path.join(sys._MEIPASS, 'exec_acq2106_hts')
    script_load_nirq = os.path.join(sys._MEIPASS, 'exec_load_nirq')
else:
    exec_path = os.path.join(os.path.abspath("."), 'exec_acq2106_hts')
    script_load_nirq = os.path.join(os.path.abspath("."), 'exec_load_nirq')


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_driver_path():
    return path


def afhba404_get_ident():
    result = subprocess.getstatusoutput(get_script(script_afhba404_get_ident))
    if result is not None and len(result) > 0:
        return result[1]
    return 'Execution failure'


def load_nirq():
    result = subprocess.getstatusoutput(script_load_nirq + ' ' + path)
    print(result)
    if result is not None and len(result) > 0:
        if result[0] == 0:
            return ResultModel.ok()
        else:
            if "File exists" in result[1]:
                return ResultModel.ok()
            else:
                return ResultModel.err(result[1])
    return ResultModel.err('Execution failure')


def mount_ramdisk():
    result = subprocess.getstatusoutput(get_script(script_mount_ramdisk))
    if result is not None and len(result) > 0:
        if result[0] == 0:
            return ResultModel.ok()
        else:
            return ResultModel.err(result[1])
    return ResultModel.err('Execution failure')


def get_ident_all():
    result = subprocess.getstatusoutput(get_script(script_get_ident_all))
    if result is not None and len(result) > 0:
        if result[0] == 0:
            if result[1] is not None and result[1] != '' and result[1].isspace() is not True:
                return ResultModel.ok(result[1].split("\n"))
            else:
                return ResultModel.ok()
        else:
            return ResultModel.err(result[1])
    return ResultModel.err('Execution failure')


def ping_acq(acq_id):
    result = subprocess.getstatusoutput('ping -c 4 {}'.format(acq_id))
    if result is not None:
        if result[0] == 0:
            return 'success'
        else:
            return 'fail'
    return 'Execution failure'


def mount_das(das_address, das_username, das_password, das_mount_path):
    file_obj = pathlib.Path(das_mount_path)
    if file_obj.exists() is not True:
        os.makedirs(das_mount_path)

    grep_result = subprocess.getstatusoutput('mount | grep {}'.format(das_address))
    if grep_result[0] == 1:
        result = subprocess.getstatusoutput(
            'mount -t cifs -o username={},password={} {} {}'.format(das_username, das_password, das_address,
                                                                    das_mount_path))
        if result is not None:
            if result[0] == 0:
                return 'success'
            else:
                return 'fail'
        return 'Execution failure'
    else:
        return 'mounted'


def change_driver_path(p):
    global path
    path = p


def acq2106_hts(args, acq_id, other):
    line = ''
    for key in args:
        if args[key] is not None and args[key] != '':
            line += '--' + key + '=' + str(args[key]) + ' '
    line += other + ' '
    line += acq_id
    s = '{} {} {} {}'.format(exec_path, path, acq2106_hts_path, line)
    print(s)
    return subprocess.Popen(s,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)


def get_script(script):
    return os.path.join(path, script)
