import os
import shutil

RUBIX_WIRES_DATA_DIR = '/data/rubix-wires'
IO_CALIBRATION_FILE = 'io-calibration.json'


def copy_io_calibration():
    if not os.path.isdir(RUBIX_WIRES_DATA_DIR):
        os.mkdir(RUBIX_WIRES_DATA_DIR)
    if not os.path.exists(f'{RUBIX_WIRES_DATA_DIR}/{IO_CALIBRATION_FILE}'):
        shutil.copy(f'config/{IO_CALIBRATION_FILE}', RUBIX_WIRES_DATA_DIR)
