from django.db import models
from django.utils import timezone
from django.conf import settings
from .wechat_api import WechatCgiApi

# Create your models here.
class WechatConfig(models.Model):

    # Configuration Keys
    KEY_MENU_JSON = "wechat_menu_json"
    KEY_ACCESS_TOKEN = "wechat_access_token"


    key = models.CharField(max_length=128, choices=(
        (KEY_MENU_JSON, KEY_MENU_JSON),
        (KEY_ACCESS_TOKEN, KEY_ACCESS_TOKEN),
        ))
    value = models.CharField(max_length=1024, null=True, blank=True)
    expire_date = models.DateTimeField(null=True, blank=True)
    
    def is_expired(self):
        return self.expire_date and self.expire_date < timezone.now()

    @classmethod
    def refresh_access_token(cls):
        api = WechatCgiApi(app_id=settings.WECHAT_APP_ID, app_secret=settings.WECHAT_APP_SECRET)
        result_api = api.get_access_token()
        if result_api and result_api[u"access_token"]:
            token = result_api[u"access_token"]
            expire_date = timezone.now() + timezone.timedelta(seconds=result_api[u"expires_in"])

            token_config, created = WechatConfig.objects.get_or_create(key=WechatConfig.KEY_ACCESS_TOKEN)
            token_config.value = token
            token_config.expire_date = expire_date
            token_config.save()

            return True, result_api
        else:
            return False, result_api

