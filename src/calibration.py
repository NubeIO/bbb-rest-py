from src.constants.meter_readings import meter_reading
import json

from src.utils.io_calibration import copy_io_calibration, RUBIX_WIRES_DATA_DIR, IO_CALIBRATION_FILE

data_json_file = f'{RUBIX_WIRES_DATA_DIR}/{IO_CALIBRATION_FILE}'
test_json_file = 'test.json'

copy_io_calibration()

with open(data_json_file, 'r') as f:
    data = f.read()

# parse file
obj = json.loads(data)

rawReads = {
    "UI1": obj['UI1'],
    "UI2": obj['UI2'],
    "UI3": obj['UI3'],
    "UI4": obj['UI4'],
    "UI5": obj['UI5'],
    "UI6": obj['UI6'],
    "UI7": obj['UI7'],
    "UI1_MA": obj['UI1_MA'],
    "UI2_MA": obj['UI2_MA'],
    "UI3_MA": obj['UI3_MA'],
    "UI4_MA": obj['UI4_MA'],
    "UI5_MA": obj['UI5_MA'],
    "UI6_MA": obj['UI6_MA'],
    "UI7_MA": obj['UI7_MA'],

}


# get last value in the calibration array
def ui_calibration_table(port):
    port = port.upper()  # To uppercase; ie values UI1, UI2, etc..
    port = port + '_MA'
    return rawReads.get(port, None)


# Scaling function
def ui_scale(port, value):
    port = port.upper()  # To uppercase; ie values UI1, UI2, etc..
    ui_raw = rawReads.get(port, None)  # UI1 default values
    # ui_raw = rawReads[port]
    if value <= ui_raw[0]:
        # calculate slope at lower bounds
        slope = (meter_reading[0] - meter_reading[1]) / (ui_raw[0] - ui_raw[1])
        # interpolate value using the slope
        value = meter_reading[0] + ((value - ui_raw[0]) * slope)
    elif value >= ui_raw[10]:
        # calculate slope at upper bounds
        slope = (meter_reading[9] - meter_reading[10]) / (ui_raw[9] - ui_raw[10])
        # interpolate value using the slope
        value = meter_reading[10] + ((value - ui_raw[10]) * slope)
    else:
        # interpolate reading when value between uiRaw[i] and uiRaw[i+1]
        for i in range(10):
            if (value >= ui_raw[i] and value <= ui_raw[i + 1]):
                slope = (meter_reading[i] - meter_reading[i + 1]) / (ui_raw[i] - ui_raw[i + 1])
                value = meter_reading[i] + ((value - ui_raw[i]) * slope)
                break
    return value / 10


point = 'UI1'
# print(ui_scale(point, 0.5))
print(ui_calibration_table(point))
