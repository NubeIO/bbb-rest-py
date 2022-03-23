# bbb-py-rest

## Running in development
- Use [`poetry`](https://github.com/python-poetry/poetry) to manage dependencies
- Simple script to install

    ```bash
    ./setup.sh
    ```

- Join `venv`

    ```
    poetry shell
    ```

- Build local binary

    ```bash
    poetry run pyinstaller run.py -n bbb-py-rest --clean --onefile --add-data pyproject.toml:.
    ```

  The output is: `dist/bbb-py-rest`
  
## Docker build

### Build

```bash
./docker.sh
```

The output image is: `bbb-py-rest:dev`

### Run

```bash
docker volume create bbb-py-rest
docker run --rm -it -p 2020:2020 -v bbb-py-rest-data:/data --name bbb-py-rest bbb-py-rest:dev
```

## Deploy on Production

- Download release artifact
- Review help and start

```bash
$ bbb-py-rest
Usage: bbb-py-rest
```

### IO calibration

- Use the RAW.py and paste into google sheets and download as a csv
- Use any text editor to open the csv as csv format as below. (`visual-code` will work)
- Use https://www.convertcsv.com/csv-to-json.htm and option `CSV To Json Column Array`
- Add the json file in `/data/rubix-wires/io-calibration.json`

```csv
UI1, UI2, UI1_MA
0.1, 0.1, 1
0.2, 0.3, 10
0.4, 0.4, null
```

Note: Version 1.4 of the Nube iO Edge Controller does not need the UART pins enabled and doing so conflicts with the pins for R1. 

### For testing

Comment out all the `Adafruit_BBIO` libs 
& uncomment the random values as below ``val = random.uniform(0, 1)  # for testing``

```python
@app.route('/api/' + api_ver + '/read/' + ui + '/<io_num>', methods=['GET'])
def read_ai(io_num=None):
    gpio = analog_in(io_num)
    if gpio == -1:
        return jsonify({'1_state': "unknownType", '2_ioNum': io_num, '3_gpio': gpio, '4_val': 'null',
                        "5_msg": analogInTypes}), http_error
    else:
        # val = ADC.read(gpio)
        val = random.uniform(0, 1)  # for testing
        return jsonify({'1_state': "readOk", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
                        '5_msg': 'read value ok'}), http_success
```

##### Block port 5000

In ip tables -A is to add and -D is to delete an entry

```
// only allow localhost access to port 5000
sudo iptables -A INPUT -p tcp -s localhost --dport 5000 -j ACCEPT
// drop all other hosts
sudo  iptables -A INPUT -p tcp --dport 5000 -j DROP
// then save the tables
!!! Not tested
https://upcloud.com/community/tutorials/configure-iptables-centos/

// to remove a rule
sudo iptables -D INPUT -p tcp --dport 5000 -j DROP
```

### API for the GPIO

### LoRa Connect Reset

This api will let you reset the power on the lora connect

```
// write the lora connect off
localhost:5000/api/1.1/write/do/lc/0/16
```
IO_TYPES
ui, uo, di, do

// read 
/read/IO_TYPE/IO_Number
// read all IOs as per type. like /read/all/ui
/read/all/IO_TYPE

```
#### Read a UI as a DI (jumper needs to be set to 10K)
off/open = around 0.9 vdc
on/closed = around 0.1 vdc

### read all
```
// read all DIs
http://0.0.0.0:5000/api/1.1/read/all/di
// read all AIs
http://0.0.0.0:5000/api/1.1/read/all/ai
```
#### UOs
https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/pwm
```
UOs 0 = 12vdc and 100 = 0vdc (Yes its backwards)
<io_num>/<val>/<pri>
uo/uo1/22/16
the priority (pri) is not supported yet but it's there for future use if needed
http://0.0.0.0:5000/api/1.1/write/uo/uo1/100/16
// this returns the values that was stored in the DB (So not reading the actual pin value)
```
#### DOs
https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/gpio
```
/<io_num>/<val>/<pri>
the priority (pri) is not supported yet but it's there for future use if needed
DOs true for high false for low
http://0.0.0.0:5000/api/1.1/write/do/do1/true/16
```
#### UIs
https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/adc
```
UIs will return a float between 0 and 1
http://0.0.0.0:5000/api/1.1/read/ui/ui1
```
#### DIs
https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/gpio
```
DIs will return a int either 0 and 1 (0 is on 1 is off)
http://0.0.0.0:5000/api/1.1/read/di/di1
```
## Cloning eMMc image to microSD card as a Flasher.
* Boot off beaglebone on eMMc you wish to clone.
* Insert a blank FAT formatted microSD card at least 4GB.
* Login to your beaglebone and run the scripts
```bash
cd /opt/scripts/tools/eMMC
sudo ./beaglebone-black-make-microSD-flasher-from-eMMC.sh
```
* Once finish, reboot and boot off the beaglebone using the microSD card as an image flasher


## install wires and bbb-rest


```
sudo systemctl stop rsyslog.service
sudo systemctl disable rsyslog.service
sudo systemctl stop syslog.socket
sudo systemctl disable syslog.socket
sudo rm -r *
git clone --depth 1 https://github.com/NubeIO/bash-scripts
sudo bash remove-services.sh debian
Download bbb-rest
wget https://github.com/NubeIO/bbb-py-rest/archive/v1.0.2.zip
unzip v1.0.2.zip 
mv bbb-py-rest-1.0.2 bbb-py-rest
cd bbb-py-rest
bash setup.bash
sudo mkdir /data
sudo mkdir /data/rubix-wires
sudo chown -R $USER:$USER /data
cd /data/rubix-wires/
mkdir config
sudo nano /data/rubix-wires/config/.env
# edit the .env file
#--------------Edge 28 config-----------------------------------------------------
PORT=1313
SECRET_KEY=__SECRET_KEY__
EDGE_28_BASEURL=localhost
EDGE_28_PORT=5000
EDGE_28_API_VER=1.1
sudo nano /data/rubix-wires/io-calibration.json
{
    "UI1":[0.01,0.02,0.04,0.07,0.1,0.2,0.3,0.4,0.6,0.8,1.0],
    "UI2":[0.01,0.02,0.04,0.07,0.1,0.2,0.3,0.4,0.6,0.8,1.0],
    "UI3":[0.01,0.02,0.04,0.07,0.1,0.2,0.3,0.4,0.6,0.8,1.0],
    "UI4":[0.01,0.02,0.04,0.07,0.1,0.2,0.3,0.4,0.6,0.8,1.0],
    "UI5":[0.01,0.02,0.04,0.07,0.1,0.2,0.3,0.4,0.6,0.8,1.0],
    "UI6":[0.01,0.02,0.04,0.07,0.1,0.2,0.3,0.4,0.6,0.8,1.0],
    "UI7":[0.01,0.02,0.04,0.07,0.1,0.2,0.3,0.4,0.6,0.8,1.0],
    "UI1_MA":[0,1,null,null,null,null,null,null,null,null,null],
    "UI2_MA":[0,1,null,null,null,null,null,null,null,null,null],
    "UI3_MA":[0,1,null,null,null,null,null,null,null,null,null],
    "UI4_MA":[0,1,null,null,null,null,null,null,null,null,null],
    "UI5_MA":[0,1,null,null,null,null,null,null,null,null,null],
    "UI6_MA":[0,1,null,null,null,null,null,null,null,null,null],
    "UI7_MA":[0,1,null,null,null,null,null,null,null,null,null]
}

```
## install wires
Add build version as a var
```
WIRES=2.1.8
```

```
wget https://github.com/NubeIO/wires-builds/archive/refs/tags/v$WIRES.zip  \
&& unzip v$WIRES.zip \
&& mv wires-builds-$WIRES wires-builds \
&& cd wires-builds/rubix-wires/systemd \
&& sudo bash script.bash install -s=nubeio-rubix-wires.service -u=debian --working-dir=/home/debian/wires-builds/rubix-wires -g=/data/rubix-wires -d=data -c=config -p=1313 \
&& cd ~
```


    
# LoRa Connect
```
stty -F /dev/ttyS1 38400 -cstopb -parenb && cat /dev/ttyS1
```


```
var b = require('bonescript');
b.pinMode('P9_41', b.OUTPUT);


function gpioLow() {
b.digitalWrite('P9_41', b.LOW);
console.log('Reseting LoRa Module. Set pin to LOW');
}

function gpioHigh() {
b.digitalWrite('P9_41', b.HIGH);
console.log('Reset LoRa Module. Set pin back to High');
}

gpioLow();

// wait after 3 seconds to set the pin back to high
setTimeout(gpioHigh, 5000);

```


