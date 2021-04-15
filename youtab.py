from tkinter import *
from changemail import switcher
import os
import sys
import random
import tool
import time
import json
import _log
import toolv2 as t2
from adbutils import adb
import uiautomator2 as u2
class YouTab:
    def __init__(self,machine_id,proxy,on_proxy):
        self.file_videos_list = "data/youtube_videos_list.txt"
        self.package_youtube = "com.google.android.youtube"
        self.package_google_gmail = "com.google.android.gms"
        self.package_hangan_manager = "com.hanganmanager.phone"
        self.log = _log.Logging("HANGANSTUDIO=%s"%machine_id)

        with open("data/configure.json","r",encoding="utf8") as fo:
            self.jout = json.load(fo)
        bool_changemail       = int(self.jout['bool:changemail'])
        self.on_proxy = on_proxy
        if on_proxy:
            (self.log).logging("info","Máy [%s] kết nối tới IP: %s"%(machine_id,proxy))

        self.subscribe_ed = False
        self.unsubscribe_ed = False
        self.comment_ed = False
        self.like_ed = False
        self.dislike_ed = False

        self.dab, self.du2 = self.connect_phone()

        (self.du2).settings['wait_timeout'] = 1

        self.log.logging('info','Đặt lại cấu hình proxy')
        os.system("adb -s %s shell settings put global http_proxy :0"%self.du2.serial)

        self.proxy = proxy
        self.macros(self.proxy)

        self.window_size = (self.du2).window_size()
        
        count = 0  
        self.cache = []
        while count < self.loop:                    
            count += 1
            
            if bool_changemail:
                email_selected = switcher(t2, self.du2, self.dab, cache=self.cache)
                self.cache.append(email_selected)
            
            self.watching()
            if count < self.loop:
                self.macros(self.proxy)
            self.execute_root_command()
            
        (self.log).logging('info','Đã hoàn thành các vòng lặp')
    def macros(self,proxy):
        (self.log).logging('info','Bắt đầu khởi chạy')
        self.check_screen_on()
        self.check_installed()
        if self.on_proxy:
            self.log.logging('info','Connecting %s'%proxy)
            os.system("adb -s %s shell settings put global http_proxy %s"%(self.du2.serial,proxy))
        self.open_youtube()
        self.check_settings()
        (self.log).logging('info','Khởi tạo vòng lặp')
        
    def execute_root_command(self):
        with open("cmd/__cmd__","r") as fo:
            out = fo.read().strip()
        if out.find("return youtube main activity")>=0:
            (self.log).logging('info','Hệ thống: %s'%out)
            self.macros(self.proxy)
            with open("cmd/__cmd__","w+") as fi:
                fi.write("")
            sys.exit(0)
            
    def watching(self):
        if not os.path.exists(self.file_videos_list):
            (self.log).logging('error','File %s not found'%self.file_videos_list)
            os._exit(-2)
        with open(self.file_videos_list,"r",encoding="utf8") as fo:
            videos = [e.strip() for e in fo.readlines()]
        self.first_time = True
        for i in range(len(videos)):
            self.reset_ed()
            self.check_screen_on()
            self.check_settings()

            def macro_search():
                (self.log).logging('info','Bắt đầu tìm kiếm')
                if self.first_time:
                    tool.click_byXpath(self.du2,'//*[@resource-id="com.google.android.youtube:id/menu_item_1"]',note="click vao o search")
                    self.first_time = False
                else:
                    (self.du2).drag(180,300,600,900)
                    tool.click_byXpath(self.du2,'//*[@resource-id="com.google.android.youtube:id/search_query"]')
                with open("data/keywords.txt","r",encoding="utf8") as fo:
                    keywords = [e.strip() for e in fo.readlines()]
                keyword = random.choice(keywords)
                (self.log).logging('info',"Nhập từ khóa: %s"%keyword)
                (self.du2).clear_text()
                (self.du2).send_keys(keyword)
                (self.du2).press("enter")
            if self.search:
                macro_search()
            if self.randb:
                if random.randint(1,int(self.jout['probability:misleading_2'].split("1/")[1])) == 2:
                    macro_search()
                    
            self.misleading_1()
            (self.log).logging('info','Bắt đầu xem liên kết video')
            video = random.choice(videos)
            (self.log).logging('info','Mở liên kết %s'%video)
            (self.dab).open_browser(video)
            time.sleep(random.randint(1,3))
            tool.click_byXpath(self.du2,'//*[@resource-id="android:id/button_always"]',_limit=4)
            
            count = 0
            limit = 3
            while not (self.du2).xpath('//*[@resource-id="com.google.android.youtube:id/skip_ad_button_container"]').exists:
                (self.log).logging('info','Đang tải video...')
                t2.xpwclick(self.du2,'//*[@resource-id="com.google.android.youtube:id/player_control_play_pause_replay_button"]',note="play if it pausing")
                count += 1
                if count >= limit: break
                if (self.du2).xpath('//*[@resource-id="com.google.android.youtube:id/skip_ad_button_icon"]').exists: break
                # self.execute_root_command()
            if (self.du2).xpath('//*[@resource-id="com.google.android.youtube:id/skip_ad_button_text"]').exists\
                    or (self.du2).xpath('//*[@resource-id="com.google.android.youtube:id/skip_ad_button_container"]').exists:
                (self.log).sleep(self.time_ads_watch)
                if not tool.click_byXpath(self.du2,'//*[@resource-id="com.google.android.youtube:id/skip_ad_button_container"]',_limit=2):
                    (self.log).logging('ERROR','Không có quảng cáo cần được bỏ qua')
            (self.log).logging('info','Tiêu đề video: %s'%self.check_video_title())
            
            self.naughty()
            # self.execute_root_command()
            
        (self.log).logging('info','Hoàn thành quá trình xem')
        
    def check_video_title(self,left=30):
        self.log.logging('info', 'Kiểm tra tiêu đề video: left=%d'%left) 
        try:
            return (self.du2).xpath('//*[@resource-id="com.google.android.youtube:id/title"]').text
        except Exception as err:
            (self.log).logging('error',(self.check_video_title).__name__+" -> %s"%err)
            (self.log).sleep(5.0)
            try:
                (self.du2)(scrollable=True).scroll.vert.toBeginning(steps=100)
            except Exception as err:
                self.log.logging('debug', 'HA NGAN TOOL CANNOT SCROLL: %s'%err)          
            self.check_video_title(left=left-1)
            
    def botlike(self,_type):
        # self.execute_root_command()
        current_video_title = self.check_video_title()
        (self.log).logging('info','Tiêu đề video đang xem: %s'%current_video_title)
        if _type == 'like':
            with open("data/title_videos_liked.txt","r",encoding="utf8") as fo:
                list_titles = [e.strip() for e in fo.readlines()]
            if current_video_title not in list_titles:
                (self.log).logging('info','Đã Like video này')
                if tool.click_byXpath(self.du2,'//*[@resource-id="com.google.android.youtube:id/like_button"]'):
                    time.sleep(random.randint(1,3))
                    with open("data/title_videos_liked.txt","a+",encoding="utf8") as fa:
                        fa.write(current_video_title+"\n")
        elif _type == 'dislike':
            with open("data/title_videos_disliked.txt","r",encoding="utf8") as fo:
                list_titles = [e.strip() for e in fo.readlines()]
            if current_video_title not in list_titles:
                (self.log).logging('info','Đã Dislike video này')
                if tool.click_byXpath(self.du2,'//*[@resource-id="com.google.android.youtube:id/dislike_button"]'):
                    time.sleep(random.randint(1,3))
                    with open("data/title_videos_disliked.txt","a+",encoding="utf8") as fa:
                        fa.write(current_video_title+"\n")
        elif _type == 'subscribe':
            (self.log).logging('info','Đã Subscribe video này')
            tool.click_byXpath(self.du2,'//*[@resource-id="com.google.android.youtube:id/subscribe_button"]',_limit=4)
            tool.click_byXpath(self.du2,'//*[@resource-id="android:id/button2"]',_limit=4)
            (self.log).sleep(3.0)
        elif _type == 'unsubscribe':
            (self.log).logging('info','Đã Unsubscribe video này')
            tool.click_byXpath(self.du2,'//*[@resource-id="com.google.android.youtube:id/subscribe_button"]',_limit=4)
            tool.click_byXpath(self.du2,'//*[@resource-id="android:id/button1"]')
            (self.log).sleep(3.0)
        elif _type == 'comment':
            (self.log).logging('info','Đã Comment video này')
            (self.log).sleep(3.0)
            if t2.xpwait(self.du2,'//*[@content-desc="Tính năng bình luận đã bị tắt. Tìm hiểu thêm"]'):
                self.log.logging('info','Comment -> Video bị tắt tính năng này')
                return
            if not (self.du2).xpath('//*[@content-desc="Bình luận công khai..."]').exists:
                tool.click_byXpath(self.du2,'//*[@resource-id="com.google.android.youtube:id/watch_list"]/android.view.ViewGroup[1]',_limit=4)
                # tool.click_byXpath(self.du2,'//*[@resource-id="com.google.android.youtube:id/watch_list/android.view.View[1]"]',_limit=4)
            (self.log).sleep(3.0)
            back = False
            if not tool.click_byXpath(self.du2,'//*[@content-desc="Bình luận công khai..."]'):
                (self.log).sleep(1)
                if not (self.du2).xpath('//*[@content-desc="Tính năng bình luận đã bị tắt. Tìm hiểu thêm"]').exists:
                    try:
                        (self.du2)(scrollable=True).scroll.vert.toBeginning()
                    except Exception as err:
                        self.log.logging('info', 'HA NGAN TOOL CANNOT SCROLL: %s'%err)
                    tool.click_byXpath(self.du2,'//*[@content-desc="Bình luận công khai..."]')
                    back = True
            (self.log).sleep(3.0)
            with open("data/comperm/perm.p","r",encoding="utf8") as fo:
                perm = fo.read().strip()
            _t_deadline = 10
            t = time.time()    
            while perm.find("victory")<0:
                if (time.time() - t) > _t_deadline:
                    self.log.logging('debug', 'HA NGAN TOOL TIMEOUT BREAK')
                    break 
                (self.log).logging('debug','Đang tiến hành ghi lại -> vui lòng chờ')
                time.sleep(random.randint(1,3))
                with open("data/comperm/perm.p","r") as fo:
                    perm = fo.read()
                    
            with open("data/comperm/perm.p","w+") as fi:
                fi.write("defeat")

            with open("data/temp/comment.used","r",encoding="utf8") as fo:
                used_out_lines = [e.strip() for e in fo.readlines()]
            
            with open("data/comments.txt","r",encoding="utf8") as fo:
                out_lines = [e.strip() for e in fo.readlines()]

            if out_lines:
                comment_selected = random.choice(out_lines)
                t = time.time()
                _t__deadline = 10 
                while comment_selected in used_out_lines:
                    if (time.time() - t) > _t_deadline:
                        break 
                    (self.log).logging('info','Đang lựa chọn một bình luận ngẫu nhiên')
                    comment_selected = random.choice(out_lines)
                    
                if not comment_selected:
                    comment_selected = "Video hay lắm bạn ơi !"

                (self.log).sleep(3.0)
                for char in comment_selected:
                    self.du2.send_keys(char) 
                              
                tool.click_byXpath(self.du2,'//*[@resource-id="com.google.android.youtube:id/send_button"]')
                out_lines.remove(comment_selected)
                with open("data/comments.txt","w+",encoding="utf8") as fi:
                    fi.writelines([e+"\n" for e in out_lines])
                with open("data/temp/comment.used","a+",encoding="utf8") as fa:
                    fa.write(comment_selected+"\n")
                with open("data/comperm/perm.p","w+") as fi:
                    fi.write("victory")

                (self.log).sleep(3,'update')
            else:
                (self.log).logging('debug','Không còn dữ liệu bình luận để tiến hành bình luận')

                with open("data/comperm/perm.p","w+") as fi:
                    fi.write("victory")
                time.sleep(0.5)
                (self.du2).click(self.window_size[0]/2,self.window_size[1]/3)
            tool.click_byXpath(self.du2,'//*[@resource-id="com.google.android.youtube:id/close_button"]')
            if back:
                (self.log).sleep(1.2)
                try:
                    (self.du2)(scrollable=True).scroll.vert.toBeginning(steps=100)
                except Exception as err:
                    self.log.logging('debug', "HA NGAN TOOL CANNOT SCROLL: %s"%err)
        else:
            (self.log).logging('error','Chế độ ngẫu nhiên chưa xác định')
            
    def check_range(self):
        return [x.strip() for x in [e.attrib['content-desc'] for e in (self.du2).xpath("//android.widget.SeekBar").all()][0].split("/")]
        
    def naughty(self):
        def _pause(_tsleep):
            ws = self.window_size
            (self.log).execute_function('',(self.du2).click,ws[0]/2,ws[1]/6)
            (self.log).sleep(3.0)
            (self.log).execute_function('pause',(self.du2).click,ws[0]/2,ws[1]/6)
            (self.log).sleep(_tsleep+1.5)
            (self.log).execute_function('resumse',(self.du2).click,ws[0]/2,ws[1]/6)
        with open("data/configure.json","r",encoding="utf8") as fo:
            _jout = json.load(fo)
        probability_misleading_2 = int(_jout['probability:misleading_2'].split("1/")[1])

        bool_random       = int(_jout['bool:random'])
        bool_like         = int(_jout['bool:like'])
        bool_dislike      = int(_jout['bool:dislike'])
        bool_subscribe    = int(_jout['bool:subscribe'])
        bool_unsubscribe  = int(_jout['bool:unsubscribe'])
        bool_comment      = int(_jout['bool:comment'])

        delay_random      = int(_jout['delay:sec:random'])
        delay_like        = int(_jout['delay:sec:like'])
        delay_dislike     = int(_jout['delay:sec:dislike'])
        delay_subscribe   = int(_jout['delay:sec:subscribe'])
        delay_unsubscribe = int(_jout['delay:sec:unsubscribe'])
        delay_comment     = int(_jout['delay:sec:comment'])

        _tcount = 0
        (self.log).logging('info','Watching this video in %s seconds'%self.time_watch)
        probability_like = int(_jout['probability:like'].split("1/")[1])
        probability_subscribe = int(_jout['probability:subscribe'].split("1/")[1])
        probability_comment = int(_jout['probability:comment'].split("1/")[1])
        while 1:
            t1 = time.time()
            try:
                current_time, total_time = self.check_range()
            except:
                current_time = total_time = "unknown"
            (self.log).logging('info','Video của bạn đang xem được %s giây / Thời gian dự tính trong khoảng / %s / %s'%(_tcount, current_time,total_time))
            if current_time == total_time:
                (self.log).logging('error','Đã hoàn tất xem danh sách videos')
                break
            if random.randint(1,probability_misleading_2) == 1:
                (self.log).logging('info','Đang tiền hành lựa chọn ngẫu nhiên')
                self.misleading_2()
            if random.randint(1,1100) == 1:
                (self.log).logging('info','Đang ngẫu nhiên tạm dừng video')
                _pause(random.randint(1,3))
            t2 = time.time()
            _tcount += t2-t1
            _tcount = round(_tcount,3)
            if _tcount >= self.time_watch:
                (self.log).logging('info','Hoàn thành quá trình xem !')
                break
            if bool_random:
                if random.randint(1,probability_comment) == 1:
                    if _tcount >= delay_comment:
                        try:
                            self.botlike('comment')
                        except Exception as err:
                            (self.log).logging('error',err)
                if random.randint(1,probability_like) == 1:
                    if _tcount >= delay_like and not self.like_ed:
                        self.botlike('like')
                        self.like_ed = True
                if bool_dislike:
                    if _tcount >= delay_dislike and not self.like_ed:
                        self.botlike('dislike')
                        self.dislike_ed = True
                if random.randint(1,probability_subscribe) == 1:
                    if _tcount >= delay_subscribe:
                        self.botlike('subscribe')
                        self.subscribe_ed = True
                if bool_unsubscribe:
                    if _tcount >= delay_unsubscribe:
                        self.botlike('unsubscribe')
            else:
                if bool_comment:
                    if _tcount >= delay_comment and not self.comment_ed:
                        try:
                            self.botlike('comment')
                        except Exception as err:
                            (self.log).logging('error',err)
                        self.comment_ed = True
                if bool_like:
                    if _tcount >= delay_like and not self.like_ed:
                        self.botlike('like')
                        self.like_ed = True
                if bool_dislike:
                    if _tcount >= delay_dislike and not self.like_ed:
                        self.botlike('dislike')
                        self.dislike_ed = True
                if bool_subscribe and not self.subscribe_ed:
                    if _tcount >= delay_subscribe:
                        self.botlike('subscribe')
                        self.subscribe_ed = True
                if bool_unsubscribe and not self.unsubscribe_ed:
                    if _tcount >= delay_unsubscribe:
                        self.botlike('unsubscribe')
                        self.unsubscribe_ed = True
            # self.execute_root_command()
            
    def misleading_2(self):
        (self.log).logging('info','Bắt đầu quá trình xem lại')
        if random.randint(1,500) == 8:
            tool.click_byXpath(self.du2,'//*[@resource-id="com.google.android.youtube:id/expansion_icon"]',_limit=2)
        ws = self.window_size
        (self.du2).drag(ws[0]/2,ws[1]/6,ws[0]/2,ws[1])
        self.misleading_1()
        self.execute_root_command()
        
    def misleading_1(self):
        (self.log).logging('info','Bắt đầu quá trình xem')
        lucky = random.randint(2,5)
        for i in range(lucky):
            _rstep = random.randint(20,80)
        try:
            (self.du2)(scrollable=True).scroll(step=_rstep)
        except Exception as err:
            self.log.logging('debug', 'HA NGAN TOOL CANNOT SCROLL: %s'%err)
            time.sleep(random.random()*random.randint(1,2))
            self.execute_root_command()
            
    def connect_phone(self):
        _dlist = adb.device_list()
        if len(_dlist) > 1:
            serial_list = [i.serial for i in _dlist]
            for current_serial in serial_list:
                with open("data/temp/devices_using.txt","r") as fo:
                    _devus = [e.strip() for e in fo.readlines()]
                if current_serial in _devus:
                    (self.log).logging('info',"Điện thoại[%s] đã sằn sàng chạy "%current_serial)
                else:
                    (self.log).logging('info',"Thiết bị [%s] được lựa chọn "%current_serial)
                    with open("data/temp/devices_using.txt","a+") as fa:
                        fa.write(current_serial+"\n")
                    try:
                        result = [adb.device(serial=current_serial),u2.connect(current_serial)]
                    except Exception as err:
                        result = ['','']
                        (self.log).logging('fatal','Kết nối đến điện thoại bị lỗi: %s'%err)
                    return result
        else:
            return [adb.device(),u2.connect()]
            
    def check_settings(self):
        if not os.path.exists("data/configure.json"):
            temp_json_data = {
                    "watch:sec:min=": 30,
                    "watch:sec:max=": 60,
                    "ads:sec:min=": 5,
                    "ads:sec:max=": 15,
                    "loop": 1
                    }
            with open("data/configure.json","w+") as fi:
                fi.write(json.dumps(temp_json_data,indent=2))
        with open("data/configure.json","r") as fo:
            _jdata = json.load(fo)
        twmin = _jdata['watch:sec:min=']
        twmax = _jdata['watch:sec:max=']
        adsmin = _jdata['ads:sec:min=']
        adsmax = _jdata['ads:sec:max=']
        loop = _jdata['loop']
        search = _jdata['bool:search']
        changeip = _jdata['bool:changeip']
        brandom = _jdata['bool:random']
        self.time_watch = random.randint(twmin,twmax)
        self.time_ads_watch = random.randint(adsmin,adsmax)
        self.loop = loop
        self.search = search
        self.changeip = changeip
        self.randb = brandom
        
    def reset_ed(self):
        self.subscribe_ed = False
        self.unsubscribe_ed = False
        self.comment_ed = False
        self.like_ed = False
        self.dislike_ed = False
        
    def check_installed(self):
        installed_application = list((self.du2).shell("pm list packages"))[0]
        if (self.package_youtube not in installed_application):
            os.system("adb -s %s install %s"%(self.du2.serial,"data/app/com.google.android.youtube.apk"))   
        if (self.package_google_gmail not in installed_application):
            os.system("adb -s %s install %s"%(self.du2.serial,"data/app/com.google.android.gms.apk"))                       
        if (self.package_hangan_manager not in installed_application):
            os.system("adb -s %s install %s"%(self.du2.serial,"data/app/com.hanganmanager.phone.apk"))
            
    def check_screen_on(self):
        if not ((self.du2).info.get('screenOn')):
            (self.log).logging('fatal','Vui lòng bật màn hình thiết bị lên hoặc có thiết bị đã bị tắt màn hình')
            os._exit(-2) 
            
    def open_youtube(self):
        (self.du2).app_stop_all()
        (self.dab).app_start(self.package_youtube)
        _t_deadline = 15
        t = time.time()
        while not tool.click_byXpath(self.du2,'//*[@text="Trang chủ"]',_limit=2):
            if (time.time() - t) > _t_deadline: 
                (self.log).logging('info','Đang mở app YouTube trên thiết bị')
                break
            (self.log).logging('info','Đang đợi app YouTube khởi động ...')               
  
        t = time.time()
        while (self.du2).xpath('//*[@resource-id="com.google.android.youtube:id/secondary_retry_button"]').exists:    
            if (time.time() - t) > _t_deadline:        
                self.log.logging('debug', 'Thời gian khởi động app YouTube quá lâu: open_youtube()')
                break 
            (self.log).execute_function('',(self.du2).xpath('//*[@resource-id="com.google.android.youtube:id/secondary_retry_button"]').click)
