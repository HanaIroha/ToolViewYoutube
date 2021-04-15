try:
    import requests
except:
    import os
    if os.system("python -m pip install requests"):
        os.system("py -m pip install requests")
API_OPTIONS = {'TREND': 'trends',
               'PASTE': 'paste',
               'USER_PASTE': 'list',
               'DELETE_PASTE': 'delete',
               'USER_RAW_PASTE': 'show_paste'}

class DST(object):
    def __init__(self, api_dev_key=None, verify_ssl=True):
        self.api_dev_key = api_dev_key
        self.api_user_key = None
        self.verify_ssl = verify_ssl

    def checkpublicip(self):
        return requests.get("https://api.myip.com").json()
    
    def auth(self, username, password):
        data = {
            "api_dev_key": self.api_dev_key,
            "api_user_name": username,
            "api_user_password": password,
        }

        r = requests.post("https://pastebin.com/api/api_login.php", data, **self.general_params())

        self.api_user_key = r.text

        return self.api_user_key

    def crtpst(
        self,
        api_paste_code,
        api_paste_private=0,
        api_paste_name=None,
        api_paste_expire_date=None,
        api_paste_format=None,
    ):
        data = {
            "api_dev_key": self.api_dev_key,
            "api_user_key": self.api_user_key,
            "api_paste_code": api_paste_code,
            "api_paste_private": api_paste_private,
            "api_paste_name": api_paste_name,
            "api_paste_expire_date": api_paste_expire_date,
            "api_paste_format": api_paste_format,
            "api_option": API_OPTIONS["PASTE"],
        }

        # Filter data and remove dictionary None keys.
        filtered_data = {k: v for k, v in data.items() if v is not None}

        r = requests.post("https://pastebin.com/api/api_post.php", filtered_data, **self.general_params())

        return r.text

    def gupts(self, api_results_limit=None):

        data = {
            "api_dev_key": self.api_dev_key,
            "api_user_key": self.api_user_key,
            "api_results_limit": api_results_limit,
            "api_option": API_OPTIONS["USER_PASTE"],
        }

        # Filter data and remove dictionary None keys.
        filtered_data = {k: v for k, v in data.items() if v is not None}

        r = requests.post("https://pastebin.com/api/api_post.php", filtered_data, **self.general_params())

        if r.text:
            return r.text

        return "No pastes in this account"

    def gurpt(self, api_paste_key):

        data = {
            "api_dev_key": self.api_dev_key,
            "api_user_key": self.api_user_key,
            "api_paste_key": api_paste_key,
            "api_option": API_OPTIONS["USER_RAW_PASTE"],
        }

        r = requests.post("https://pastebin.com/api/api_raw.php", data, **self.general_params())

        return r.text

    def delupt(self, api_paste_key):

        data = {
            "api_dev_key": self.api_dev_key,
            "api_user_key": self.api_user_key,
            "api_paste_key": api_paste_key,
            "api_option": API_OPTIONS["DELETE_PASTE"],
        }

        r = requests.post("https://pastebin.com/api/api_post.php", data, **self.general_params())

        return r.text

    def general_params(self):
        return {
            "verify": self.verify_ssl
        }
