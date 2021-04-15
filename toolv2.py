from adbutils import adb
import uiautomator2 as u2
import _log
import subprocess
import os
import signal
import time
import random
import string
from PIL import Image
from contextlib import contextmanager
log = _log.Logging('GMAIL')
def strrand(char=3,numb=5):
    n = char
    m = numb
    return "".join([random.choice(string.ascii_lowercase) for i in range(n)]) + "".join([random.choice(string.digits) for i in range(m)])
@contextmanager
def func_timeout(tim):
    def raise_timeout(signum,frame):
        raise TimeoutError
    signal.signal(signal.SIGALRM,raise_timeout)
    signal.alarm(tim)
    try:
        yield
    except TimeoutError:
        pass
    finally:
        signal.signal(signal.SIGALRM,signal.SIG_IGN)
def adbscroll(du2,mod,duration=300):
    if mod == 'down':
        os.system("adb -s %s swipe 250 800 250 400 %s"%(du2.serial,duration))
    elif mod == 'up':
        os.system("adb -s %s swipe 250 400 250 800 %s"%(du2.serial,duration))        
def imsize(image):
    return Image.open(image).size
def imcrop(image_des,image_source,a,b,c,d):
    img = Image.open(image_source)
    left = a
    top  = b
    right = c
    bottom = d
    img_res = img.crop((left, top, right, bottom))
    img_res.save(image_des)
    return image_des
def impclick(du2,image,timeout=60,note="loading...",tsleep=3):
    log.sleep(tsleep,note=note)
    log.logging('info','Image click: %s %s'%(image,note))
    t1=time.time()
    du2.image.click(image,timeout=timeout)
    log.logging('info','delta = %s'%(time.time() - t1))
def xpsc(du2,xpath,image_picture="temp/tempic.jpg",note=""):
    try:
        log.logging('info','Screenshot -> %s'%image_picture,note=note)
        im=du2.xpath(xpath).screenshot()
        im.save(image_picture)
        return image_picture
    except Exception as err:
        log.logging('debug',err)
        return ""
def xpsend(du2,content,cls=True):
    try:
        if cls:
            log.execute_function('',du2.clear_text)
        log.execute_function('',du2.send_keys,content)
    except Exception as err:
        log.logging('error',err)
        try:
            log.execute_function('',du2(focused=True).set_text,content)
        except Exception as err:
            log.logging('error',err)
def xpwait(du2,xpath,timeout=3,note=""):
    log.logging('info','XPATH: %s -> ACCTION: waiting #timeout=%s'%(xpath,timeout))
    t1 = time.time()
    while not du2.xpath(xpath).exists:
        time.sleep(0.25)
        t2 = time.time()
        if t2 - t1 > timeout:
            return False
    return True
def xpwenclick(du2,xpath,timeout=3,note=""):
    log.logging('info','ENSURE CLICK: %s'%xpath)
    try:
        t = time.time()
        while not (du2.xpath(xpath).exists):
            if (time.time() - t ) > timeout:
                return False
        t = time.time()
        while (du2.xpath(xpath).exists):
            du2.xpath(xpath).click()
            if (time.time() - t) > timeout:
                return False
        return True
    except Exception as err:
        log.logging('debug','No such element error: %s'%err)
        return False
def xpwclick(du2,xpath,timeout=3,note=""):
    log.logging('info','Current XPATH: %s'%xpath)
    try:
        if not log.execute_function(note,du2.xpath(xpath).wait,timeout):
            log.logging('info',"CLICK -> FAILED")
            return False
        else:
            log.execute_function(note,du2.xpath(xpath).click,)
            log.logging('info',"CLICK -> SUCCEED")
            return True
    except Exception as err:
        log.logging('debug','No such element error: %s'%err)
def change_ip_by_hand(du2):
    #xpwclick(du2,'//*[@content-desc="Dữ liệu di động, Đã tắt dữ liệu di động"]')
    sp = 0, 0
    ep = 1500, 1500
    du2.drag(sp[0],sp[1],ep[0],ep[1])
    xpwclick(du2,'//*[@resource-id="com.android.systemui:id/quick_qs_panel"]/android.widget.LinearLayout[1]/android.widget.Switch[1]')
    xpwclick(du2,'//*[@resource-id="com.android.systemui:id/quick_qs_panel"]/android.widget.LinearLayout[1]/android.widget.Switch[1]')
    du2.drag(ep[0],ep[1],sp[0],sp[1])
def change_ip_by_app(du2,dab):
    package = "com.iamthesquidward.cellnetworkreset"
    packages_installed=dab.list_packages()
    if package not in packages_installed:
        log.logging('fatal', 'Please install package name %s first'%package)
        log.terminate(exit_code=-2)
    log.execute_function('',dab.app_start,package)
    xpneedtoclick='//*[@resource-id="com.iamthesquidward.cellnetworkreset:id/button"]'
    xpwclick(du2,xpneedtoclick)
    log.logging('info','Waiting...')
    while du2.xpath('//*[@resource-id="com.android.systemui:id/mobile_type"]').exists:
        pass
    while not du2.xpath('//*[@resource-id="com.android.systemui:id/mobile_type"]').exists:
        pass
    log.execute_function('',dab.app_stop,package)
def clear_data(du2,package):
    du2.app_clear(package)
def stop_all_running_app(du2):
    du2.app_stop_all()
def on_screen(du2):
    if not du2.info.get('screenOn'):
        log.execute_function('',du2.screen_on,)
def connect_device():
    list_device = adb.device_list()
    if len(list_device)>1:
        log.logging('fatal','More than a device connected')
        log.terminate(exit_code=-2)
    else:
        return [u2.connect(),adb.device()]
