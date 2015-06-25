from django.conf import settings
from django.contrib import admin, messages
from django.utils import timezone
from .models import WechatConfig
from .wechat_api import WechatCgiApi

# Register your models here.

class WechatConfigAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'expire_date', 'is_expired']
    actions = ['update_menu', 'update_access_token']

    def is_expired(self, obj):
        return obj.is_expired()

    def update_menu(self, request, queryset=None):
        result_access_token = WechatConfig.objects.filter(key=WechatConfig.KEY_ACCESS_TOKEN)
        if not result_access_token or result_access_token[0].is_expired():
            self.message_user(request, "Wechat access token already expired!", level=messages.ERROR)
        else:
            access_token = result_access_token[0].value
            result_menu = WechatConfig.objects.filter(key=WechatConfig.KEY_MENU_JSON)
            if result_menu:
                menu = result_menu[0].value
                api = WechatCgiApi(app_id=settings.WECHAT_APP_ID, app_secret=settings.WECHAT_APP_SECRET)
                result_api = api.create_custom_menu(access_token, content=menu)
                self.message_user(request, "Server response: {0}".format(result_api))
            else:
                self.message_user(request, "Wechat menu content is not configured!", level=messages.ERROR)

    def update_access_token(self, request, queryset=None):
        result_access_token = WechatConfig.objects.filter(key=WechatConfig.KEY_ACCESS_TOKEN)
        if result_access_token and not result_access_token[0].is_expired():
            self.message_user(request, "Wechat access token is not expired", level=messages.WARNING)
        
        result, message = WechatConfig.refresh_access_token()
        if result:
            self.message_user(request, "Server response: {0}".format(message))
        else:
            self.message_user(request, "Server error: {0}".format(message), level=messages.ERROR)


admin.site.register(WechatConfig, WechatConfigAdmin)
