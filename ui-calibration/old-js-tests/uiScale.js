
const uiConstants = require('./uiConstants');

exports.calUniversalInput = function(UIport, pinValue) {
    let uiRaw;
    // switch uiRaw to the specific UI port/channel
    switch (UIport) {
        case 'UI1':
            uiRaw = uiConstants.ui1Raw;
            break;
        case 'UI2':
            uiRaw = uiConstants.ui2Raw;
            break;
        case 'UI3':
            uiRaw = uiConstants.ui3Raw;
            break;
        case 'UI4':
            uiRaw = uiConstants.ui4Raw;
            break;
        case 'UI5':
            uiRaw = uiConstants.ui5Raw;
            break;
        case 'UI6':
            uiRaw = uiConstants.ui6Raw;
            break;
        case 'UI7':
            uiRaw = uiConstants.ui7Raw;
            break;
        default:
            uiRaw = uiConstants.ui1Raw;
    }
    let uiReading = uiConstants.uiReading;
    let value = pinValue;
    // add code for when value < uiRaw[0] and value > uiRaw[9]
    if (value <= uiRaw[0]){
        //calculate slope at lower bounds
        let slope = (uiReading[0] - uiReading[1]) / (uiRaw[0] - uiRaw[1]);
        //interpolate value using the slope
        value = uiReading[0] + ((value - uiRaw[0])*slope);
    } else if (value >= uiRaw[9]) {
        //calculate slope at upper bounds
        let slope = (uiReading[8] - uiReading[9]) / (uiRaw[8] - uiRaw[9]);
        //interpolate value using the slope
        value = uiReading[9] + ((value - uiRaw[9])*slope);
    }else {
    // interpolate reading when value between uiRaw[i] and uiRaw[i+1]
        for (let i = 0; i < 9; i++) {
            if (value > uiRaw[i] && value < uiRaw[i + 1]) {
                let slope = (uiReading[i] - uiReading[i + 1]) / (uiRaw[i] - uiRaw[i + 1]);
                value = uiReading[i] + ((value - uiRaw[i])*slope);
                break;
            }
        }
    }
    return value;
};
