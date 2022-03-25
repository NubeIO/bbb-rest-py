from src.constants.thermistor_const import table_10ktype2


# function converting resistor value to temperature
def calc_temp(resistor_value=None):
    if resistor_value >= 963849.00:
        return -55.00
    elif resistor_value <= 186.10:
        return 150.00
    else:
        for temp, resistor in table_10ktype2.items():
            if resistor_value >= resistor:
                # print(resistor_value, resistor)
                # print(resistor-resistor_value, resistor-table_10ktype2.get(temp-1))
                # print(temp, temp - (resistor - resistor_value) / (resistor - table_10ktype2.get(temp-1)))
                return temp - (resistor - resistor_value) / (resistor - table_10ktype2.get(temp - 1))


#####################################Testing####################################
# values = [963849, 186.10, 10000.00, 9000.00, 8000.00, 11000.00, 1000000, 100]
# for x in values:
#		print ("Resistor =  ", x, ": Temperature = ", calc_temp(x))
################################################################################

calc_temp(10000)  # sample function call
