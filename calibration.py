from meter_readings import meter_reading
from ui_readings import ui1Raw, ui2Raw, ui3Raw, ui4Raw, ui5Raw, ui6Raw, ui7Raw

rawReads = {
    "UI1": ui1Raw,
    "UI2": ui2Raw,
    "UI3": ui3Raw,
    "UI4": ui4Raw,
    "UI5": ui5Raw,
    "UI6": ui6Raw,
    "UI7": ui7Raw,
}


# Scaling function
def ui_scale(port, value):
    ui_raw = rawReads.get(port, ui1Raw)  # UI1 default values
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
    return value/10
