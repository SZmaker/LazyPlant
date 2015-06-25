import logging, json
import urllib2
import requests

log = logging.getLogger(__name__)

class WechatCgiApi(object):
    API_URL = "https://api.weixin.qq.com/cgi-bin/{0}?{1}"

    def __init__(self, app_id="", app_secret=""):
        self.app_id = app_id
        self.app_secret = app_secret

    def _get_entry(self, endpoint, param_dict):
        param_str = ""
        for k, v in param_dict.iteritems():
            param_str += "{0}={1}&".format(k, v)
        return self.API_URL.format(endpoint, param_str)

    def _send_get_request(self, url):
        # send request with urllib2
        resp = urllib2.urlopen(url)
        content = resp.read()
        # convert json data to dictionary
        try:
            return json.loads(content)
        except Exception as e:
            log.error("Get request error: {0} content:{1}".format(e, content))
            return None
        
    def _send_post_request(self, url, body):
        # send request
        #resp = urllib2.urlopen(url, data=body)
        #content = resp.read()
        r = requests.post(url, data=body)
        content = r.text

        # convert json data to dictionary
        try:
            return json.loads(content)
        except Exception as e:
            log.error("Post request error: {0} content:{1}".format(e, content))
            return None

    def _send_post_file_request(self, url, params, files):
        r = requests.post(url, data=params, files=files)
        content = r.text

        # convert json data to dictionary
        try:
            return json.loads(content)
        except Exception as e:
            log.error("Post request error: {0} content:{1}".format(e, content))
            return None


    def get_access_token(self, grant_type="client_credential"):
        url = self._get_entry("token", {"appid": self.app_id, "secret":self.app_secret, "grant_type":grant_type})
        log.debug("Get access token: {0}".format(url)) # only debug can print this url, because app secret is sensitive

        return self._send_get_request(url)

    def get_wechat_ip(self, access_token):
        url = self._get_entry("getcallbackip", {"access_token": access_token})
        log.info("Get wechat ip: {0}".format(url))

        return self._send_get_request(url)

    def create_custom_menu(self, access_token, menu_dict={}, content=None):
        url = self._get_entry("menu/create", {"access_token":access_token})
        if content:
            body = content.encode("utf-8")
        else:
            body = json.dumps(menu_dict)
        log.info("Create custom menu: {0}\nPost: {1}".format(url, body))

        return self._send_post_request(url, body)

    def create_temp_media(self, access_token, media_type, media={}):
        url = self._get_entry("media/upload", {"access_token":access_token, "type":media_type})
        return self._send_post_file_request(url, params={}, files=media)

        
        
