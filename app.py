#!flask/bin/python
from flask import Flask, jsonify, make_response
from calibration import ui_scale, ui_calibration_table
from func import command_to_bool, is_float, analog_in, analog_out, digital_in, digital_out
from io_types import analogInTypes, analogOutTypes, digitalInTypes, digitalOutTypes

# from tests.test_data import case_list_test_analogue, case_list_test_digital, fake_analogue_data, fake_digital_data

app = Flask(__name__)

# BBB GPIO Lib
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC

# DOs
GPIO.setup("P8_7", GPIO.OUT)
GPIO.setup("P8_8", GPIO.OUT)
GPIO.setup("P8_9", GPIO.OUT)
GPIO.setup("P8_10", GPIO.OUT)
GPIO.setup("P8_12", GPIO.OUT)
GPIO.setup("P9_29", GPIO.OUT)  # 'R1'
GPIO.setup("P9_12", GPIO.OUT)  # 'R2'

# UOs # UOs 0 = 0vdc and 100 = 12vdc
PWM.start("P8_13", 0, 1000, 1)  # for startup
PWM.start("P9_14", 0, 1000, 1)
PWM.start("P9_21", 0, 1000, 1)
PWM.start("P9_42", 0, 1000, 1)
PWM.start("P8_19", 0, 1000, 1)
PWM.start("P9_16", 0, 1000, 1)
PWM.start("P9_22", 0, 1000, 1)

# DIs
GPIO.setup("P9_30", GPIO.IN)  # DI1
GPIO.setup("P9_15", GPIO.IN)
GPIO.setup("P9_31", GPIO.IN)
GPIO.setup("P9_28", GPIO.IN)
GPIO.setup("P9_23", GPIO.IN)
GPIO.setup("P9_25", GPIO.IN)
GPIO.setup("P9_27", GPIO.IN)

# AIs
ADC.setup()

# API stuff
api_ver = '1.1'  # change version number as needed
uo = 'uo'
ui = 'ui'
do = 'do'
di = 'di'

# http messages
http_error = 404
http_success = 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'try again :('}), http_error)


# index page
@app.route('/', methods=['GET'])
def index_page(io_num=None, val=None):
    return jsonify({'1_state': "whats up"}), http_success


# WRITE DOs
@app.route('/api/' + api_ver + '/write/' + do + '/<io_num>/<val>/<pri>', methods=['GET'])
def write_outputs_do(io_num=None, val=None, pri=None):
    gpio = digital_out(io_num)
    io_num = io_num.upper()
    val = command_to_bool(val)
    if gpio == -1:
        return jsonify({'1_state': "unknownType", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
                        '5_msg': digitalOutTypes}), http_error
    elif val is True:
        GPIO.output(gpio, GPIO.HIGH)  # !! GPIO CALL !!!
        return jsonify({'1_state': "writeOk", '2_ioNum': io_num, '3_gpio': gpio, '4_val': int(val),
                        '5_msg': 'wrote value to the GPIO'}), http_success
    elif val is False:
        GPIO.output(gpio, GPIO.LOW)  # !! GPIO CALL !!!
        return jsonify({'1_state': "writeOk", '2_ioNum': io_num, '3_gpio': gpio, '4_val': int(val),
                        '5_msg': 'wrote value to the GPIO'}), http_success
    else:
        return jsonify({'1_state': "unknownValue", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
                        '5_msg': 'value must be a boolean an int an string 1/0 or string on/off'}), http_error


# WRITE AOs

@app.route('/api/' + api_ver + '/write/' + uo + '/<io_num>/<val>/<pri>', methods=['GET'])
def write_outputs_ao(io_num=None, val=None, pri=None):
    gpio = analog_out(io_num)
    io_num = io_num.upper()
    if gpio == -1:
        return jsonify({'1_state': "unknownType", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
                        "5_msg": analogOutTypes}), http_error
    elif is_float(val):
        val = float(val)
        if 0 <= val <= 100:
            PWM.set_duty_cycle(gpio, val)  # !! GPIO CALL !!!
            return jsonify({'1_state': "writeOk", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
                            '5_msg': 'wrote value to the GPIO'}), http_success
        else:
            return jsonify({'1_state': "unknownRange", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
                            '5_msg': 'val must be >=0 and <=100'}), http_success
    else:
        return jsonify({'1_state': "unknownValue", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
                        '5_msg': 'value must be a float'}), http_error


# READ DIs
@app.route('/api/' + api_ver + '/read/' + di + '/<io_num>', methods=['GET'])
def read_di(io_num=None):
    gpio = digital_in(io_num)
    if gpio == -1:
        return jsonify({'1_state': "unknownType", '2_ioNum': io_num, '3_gpio': gpio, '4_val': 'null',
                        "5_msg": digitalInTypes}), http_error
    else:
        val = GPIO.input(gpio)  # !! GPIO CALL !!!
        # val = fake_digital_data()  # !!! FOR TESTING !!!
        return jsonify({'1_state': "readOk", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
                        '5_msg': 'read value ok'}), http_success


#  READ UIs
@app.route('/api/' + api_ver + '/read/' + ui + '/<io_num>', methods=['GET'])
def read_ai(io_num=None):
    gpio = analog_in(io_num)
    min_range = ui_calibration_table(io_num)[0]
    max_range = ui_calibration_table(io_num).pop()
    print(11111)
    print(min_range)
    print(max_range)
    if gpio == -1:
        return jsonify({'1_state': "unknownType", '2_ioNum': io_num, '3_gpio': gpio, '4_val': 'null',
                        "5_msg": analogInTypes}), http_error
    else:
        print(io_num)
        print(gpio)
        val = ui_scale(io_num, ADC.read(gpio))  # !!! GPIO CALL !!!
        print(2222)
        print(val)
        # val = fake_analogue_data()  # !!! FOR TESTING !!!
        return jsonify({'1_state': "readOk", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
                        '5_msg': 'read value ok', '6_min_range': min_range, '7_max_range': max_range}), http_success


# READ ALL DIs
@app.route('/api/' + api_ver + '/read/all/' + di, methods=['GET'])
def read_di_all():
    # case_list = case_list_test_digital  # !!! FOR TESTING !!!
    case_list = {}
    for key, value in digitalInTypes.items():
        case = {"val": GPIO.input(value)}
        case_list[key] = case
    return jsonify({'1_state': "readOk", '2_ioNum': "all", '3_gpio': "all", '4_val': case_list,
                    '5_msg': 'read DIs ok'}), http_success


# READ ALL UIs
@app.route('/api/' + api_ver + '/read/all/' + ui, methods=['GET'])
def read_ai_all():
    # case_list = case_list_test_analogue  # !!! FOR TESTING !!!
    case_list = {}
    min_range_array = {}
    max_range_array = {}
    for key, value in analogInTypes.items():
        case = {"val": ui_scale(key, ADC.read(value))}
        case_list[key] = case
        min_range_array[key] = ui_calibration_table(key)[0]
        max_range_array[key] = ui_calibration_table(key).pop()
    return jsonify({'1_state': "readOk", '2_ioNum': "all", '3_gpio': "all", '4_val': case_list,
                    '5_msg': 'read UIs ok', '6_min_range': min_range_array,
                    '7_max_range': max_range_array}), http_success


if __name__ == '__main__':
    app.run(host='0.0.0.0')

#
# # READ ALL DOs
# @app.route('/api/' + api_ver + '/read/all/' + do, methods=['GET'])
# def read_do_all():
#     case_list = {}
#     for item in do_table:
#         case = {"val": item['val']}
#         case_list[item['ioNum']] = case
#     return jsonify({'1_state': "readOk", '2_ioNum': "all", '3_gpio': "all", '4_val': case_list,
#                     '5_msg': 'read DOs ok'}), http_success
#
#
# # READ ALL AOs
# @app.route('/api/' + api_ver + '/read/all/' + uo, methods=['GET'])
# def read_ao_all():
#     case_list = {}
#     for item in ao_table:
#         case = {"val": item['val']}
#         case_list[item['ioNum']] = case
#     return jsonify({'1_state': "readOk", '2_ioNum': "all", '3_gpio': "all", '4_val': case_list,
#                     '5_msg': 'read UOs ok'}), http_success
#
#
# # READ A DO
#
# @app.route('/api/' + api_ver + '/read/' + do + '/<io_num>', methods=['GET'])
# def read_do(io_num=None):
#     gpio = digital_out(io_num)
#     io_num = io_num.upper()
#     if gpio == -1:
#         return jsonify({'1_state': "unknownType", '2_ioNum': io_num, '3_gpio': gpio, '4_val': 'null',
#                         "5_msg": digitalOutTypes}), http_error
#     else:
#         result = do_table.get(Query()['gpio'] == gpio)
#         val = result.get("val")
#         return jsonify({'1_state': "readOk", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
#                         '5_msg': 'read value ok'}), http_success
#
#
# # READ A AO
#
# @app.route('/api/' + api_ver + '/read/' + uo + '/<io_num>', methods=['GET'])
# def read_ao(io_num=None):
#     gpio = analog_out(io_num)
#     io_num = io_num.upper()
#     if gpio == -1:
#         return jsonify({'1_state': "unknownType", '2_ioNum': io_num, '3_gpio': gpio, '4_val': 'null',
#                         "5_msg": digitalOutTypes}), http_error
#     else:
#         result = ao_table.get(Query()['gpio'] == gpio)
#         val = result.get("val")
#         return jsonify({'1_state': "readOk", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
#                         '5_msg': 'read value ok'}), http_success
