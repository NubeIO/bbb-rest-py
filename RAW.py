import Adafruit_BBIO.ADC as ADC
ADC.setup()
from time import sleep
ui1 = "P9_39"
ui2 = "P9_40"
ui3 = "P9_37"
ui4 = "P9_38"
ui5 = "P9_33"
ui6 = "P9_36"
ui7 = "P9_35"
while (1):
    ui1Raw = ADC.read(ui1)
    ui2Raw = ADC.read(ui2)
    ui3Raw = ADC.read(ui3)
    ui4Raw = ADC.read(ui4)
    ui5Raw = ADC.read(ui5)
    ui6Raw = ADC.read(ui6)
    ui7Raw = ADC.read(ui7)
    print(ui1Raw)
    print(ui2Raw)
    print(ui3Raw)
    print(ui4Raw)
    print(ui5Raw)
    print(ui6Raw)
    print(ui7Raw)
    sleep(2)
