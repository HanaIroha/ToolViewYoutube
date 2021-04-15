import random
import time
import os
import json
import random
import datetime
import webbrowser
import uiautomator2 as u2
import _log
from adbutils import adb
from subprocess import check_output
log = _log.Logging('tool')
def fair_cake_cutting(number_id,file_contain_list):
    with open(file_contain_list,"r",encoding="utf8") as fo:
        lines = [e.strip() for e in fo.readlines()]
    number_elements = len(lines)
    result = {}
    tester = False
    if number_id == number_elements:
        for i in range(number_id):
            result[i] = lines[i]
        tester = True
    elif number_id < number_elements:
        list_used = []
        for i in range(number_id):
            e = random.choice(lines)
            while e in list_used:
                e = random.choice(lines)
            result[i] = e
            list_used.append(e)
        tester = True
    else:
        tester = False
    return [tester,result]
def get_number_devices_connected():
    return len(adb.device_list())
def click_byText(du2,text,count_out=20):
    try:
        temp = du2.xpath("//android.widget.TextView").all()
        while not temp:
            print("[DEBUG] Wait for text view widget visible")
            timme.sleep(3.0)
            temp = du2.xpath("//android.widget.TextView").all()
        for e in temp:
            print(f"[DEBUG] Widget text: {e.text}")
            if e.text.find(text)>=0:
                point = e.center()
                break
        du2.click(point[0],point[1])
    except Exception as err:
        print(f"[DEBUG] ERROR: {err}")
        return False

def click_byXpath(du2,xpath,_limit=12,_time_sleep=0,note=""):
    count = 0
    while not du2.xpath(xpath).exists:
        time.sleep(3.0)
        if count >= _limit:
            log.logging('debug','Xpath: %s not found'%xpath)
            return False
        count += 1
    try:
        du2.xpath(xpath).click()
        log.logging('info','Xpath: %s -> clicked'%xpath)
        time.sleep(_time_sleep)
        return True
    except Exception as err:
        print(f"[ERROR] {err}")
        log.logging('error',err)
        return False
def connect_android_debugger():
    log.logging('info','Connecting to android system')
    try:
        dl = adb.device_list()
        if len(dl)>1:
            i = 1
            dx = {}
            for d in dl:
                dx[i] = d.serial
                i += 1
            for x in list(dx):
                print(f"[{x}] "+dx[x])
            choice = input("Choice a number: ")
            try:
                device_serial_selected = dx[int(choice)]
            except Exception as err:
                log.logging('fatal',err)
                os._exit(-2)
            return [u2.connect(device_serial_selected),adb.device(serial=device_serial_selected)]
        else:
            return [u2.connect(),adb.device()]
    except Exception as err:
        log.logging('error',err)
        return []
def continuous_in(n, m):
    def _f(x):
        for _ in "|/-\\":
            print(f"[{_}]",end=f" Continuous in {x}"+" "*50+"\r")
            time.sleep(3.0)
    limit = random.randint(n,m)
    count = 0
    while count <= limit:
        _f(limit-count)
        count += 1
    print("\r")

def just_read(file_name):
    with open(file_name, "r") as fo:
        result = fo.read()
    return result

def just_write(file_name, content):
    with open(file_name, "w+") as fi:
        fi.write(content)

def just_append(file_name, content):
    with open(file_name, "a+") as fa:
        fa.write(content)

def just_json(file_name):
    with open(file_name, "r") as fo:
        _result_json = json.load(fo)
    return _result_json

def just_lines(file_name):
    _lines = []
    with open(file_name, "r") as fo:
        _lines = fo.readlines()
    return _lines

def number_lines(file_name):
    count = 0
    fo = open(file_name, 'r')
    while 1:
        buffer = fo.read(8192*1024)
        if not buffer: break
        count += buffer.count('\n')
    fo.close()
    return count

def current_wifi_name():
    scan_output = check_output(["iwlist", "wlan0", "scan"]).split()
    for _line in scan_output:
        _line = _line.decode()
        if _line.find("ESSID")>=0:
            return (_line.split(":")[1].split("\"")[1])

def increment_datetime(dt, days, x):
    "dt: yyyy-mm-dd"
    "x is 1 or -1"
    _y = int(dt.split("-")[0])
    _m = int(dt.split("-")[1])
    _d = int(dt.split("-")[2])
    return (datetime.datetime(_y,_m,_d)+x*datetime.timedelta(days=days)).strftime("%Y-%m-%d")

def date_to_dayofweek(dt):
    "dt: yyyy-mm-dd"
    _week = (
            "thứ 2      #monday",
            "thứ 3      #tuesday",
            "thứ 4      #wednesday",
            "thứ 5      #thursday",
            "thứ 6      #friday",
            "thứ 7      #saturday",
            "chủ nhật   #sunday"
            )
    _y = int(dt.split("-")[0])
    _m = int(dt.split("-")[1])
    _d = int(dt.split("-")[2])
    return dict(zip(tuple([x for x in range(0,7)]), _week))[datetime.datetime(_y,_m,_d).weekday()]

def how_many_days(from_dayofweek_1, to_dayofweek_2):
    """
        Input: số integer
        Ngày trong tuần bắt đầu từ thứ hai là 0,
        kết thúc ở chủ nhật là 6,sau đó lặp lại
        chu kỳ.
    """
    def next_dayofweek(current_dayofweek):
        c = current_dayofweek
        if c == 6: return 0
        else: return c+1
    f = from_dayofweek_1
    t = to_dayofweek_2
    count = 0
    while next_dayofweek(f)!=t:
        count += 1
        f = next_dayofweek(f)
    return count + 1
def browser_debug(text,tmin=3,tmax=5):
    _debug_html_file = "debug.html"
    with open(_debug_html_file, "w+") as fi:
        fi.write(text)
    webbrowser.open(_debug_html_file)
    continuous_in(tmin,tmax)
    os.remove(_debug_html_file)
