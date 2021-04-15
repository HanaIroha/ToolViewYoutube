import time, os, random
def switcher(t2, du2, dab, cache=[]):
    """
        dang o trang chu youtube
    """

    assert type(cache) == list

    ytb_pkg = "com.google.android.youtube"

    if du2.info['currentPackageName'] == ytb_pkg:
        pass



    xpath_tk = '//*[@resource-id="com.google.android.youtube:id/mobile_topbar_avatar"]'
    t2.xpwenclick(du2, xpath_tk, timeout=60)

    time.sleep(2)
    xpath_sign = '//*[@resource-id="com.google.android.youtube:id/account_container"]'
    if not t2.xpwclick(du2, xpath_sign):
        return 
    
    time.sleep(2) 

    def _m_swipe():
        """
            trong pham vi o tai khoan
        """
        xpath_tkconf = '//*[@resource-id="com.google.android.youtube:id/account_name_container"]'
        p = du2.xpath(xpath_tkconf).center()
        du2.swipe(500,700,500,500)
        input("next ?")


    def _m_scan():
        xpath_toscan = '//android.widget.TextView'
        le = [e for e in du2.xpath(xpath_toscan).all()]
        assert le

        r = {}
        c = None
        for e in le:
            ### DEBUG IF ERROR
            #print(e.text)
            if e.text.find("@")>=1:
                r[e.text] = []
                c = e.text
            if e.text.find("có")>=0:
                try:
                    r[c].append(e)
                except:
                    print("Ignore: %s"%e.text)

        return r

    r = _m_scan()
    while not r:
        print("SCANNING...")
        time.sleep(0.5)
        r = _m_scan()

    number_emails = len(r)
    print("NUMBER EMAILS FOUND: %d"%number_emails)

    list_emails = r
    for email in list_emails:
        if email in cache:
            print("IGNORE: %s"%email)
        else:
            print("SELECT: %s"%email)
            try:
                list_emails[email][0].click()
                return email
            except Exception as err:
                print(err) 
                continue 
