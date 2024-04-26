acq_id = ''
run_args = {
    'spad': '1,16,0',
    'commsA': 'all',
    'decimate': '1',
    'trg': 'ext,rising',
    'secs': 1
}
run_args_other = ''
running = False
receiving = False


def set_acd_id(val):
    global acq_id
    acq_id = val


def get_acd_id():
    return acq_id


def set_args(args):
    global run_args
    run_args = args


def get_args():
    return run_args


def set_args_other(val):
    global run_args_other
    run_args_other = val


def get_args_other():
    return run_args_other


def set_running(val):
    global running
    running = val


def get_running():
    return running


def set_receiving(val):
    global receiving
    receiving = val


def get_receiving():
    return receiving
