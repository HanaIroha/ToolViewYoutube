import time
import os
import datetime
class Logging:
    def __init__(self,branch):
        self.file_log = "log/runtime.log"
        self.branch = branch.upper()

        if not os.path.exists("log"):
            os.mkdir("log")
    def terminate(self,exitcode=-1):
        os._exit(exitcode)
    def set_breakpoint(self,note=""):
        input(self.logging('info','Breakpoint %s '%note))
    def clean(self):
        if os.path.exists(self.file_log):
            with open(self.file_log,"w+") as fi:
                fi.write("")
    def sleep(self,timeout,note=""):
        (self.logging)('info','Sleep in '+str(timeout)+' seconds',note=note,prt=False)
        time.sleep(timeout)
    def logging(self,log_level,log_content,note="",prt=True):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        if log_level=='info':
            template = f"[I {current_time} {self.branch}] {log_content}"
        elif log_level=='debug':
            template = f"[D {current_time} {self.branch}] {log_content}"
        elif log_level=='error':
            template = f"[E {current_time} {self.branch}] {log_content}"
        elif log_level=='warning':
            template = f"[W {current_time} {self.branch}] {log_content}"
        elif log_level=='fatal':
            template = f"[F {current_time} {self.branch}] {log_content}"
        else:
            template =f"[C {current_time} Logging] log_level=%s log_content=%s #unknown log_level"%(log_level,log_content)
        if note:
            template = template + " #"+note
        if prt:
            print(template)
        if os.name == 'posix':
            with open(self.file_log,"a+") as fa:
                fa.write(template+"\n")
        return template
    def execute_function(self,note,function,*args,**kwargs):
        self.logging('info',f"Call -> {function.__name__}{args}",note=note)

        t1 = time.time()
        _return = function(*args,**kwargs)
        t2 = time.time()
        delta = str(round(t2-t1,3))

        self.logging('info',f"\t* Return -> {_return}")
        self.logging('info',f"\t* Time complete: {delta} seconds")

        return _return
    def exf(self,note,function,*args,**kwargs):
        self.execute_function(note,function,*args,**kwargs)
