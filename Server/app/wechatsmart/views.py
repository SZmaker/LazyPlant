# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import logging
log = logging.getLogger(__name__)

from wechat_sdk import WechatBasic
from wechat_sdk.messages import (
    TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage
)
from .models import WechatConfig
from .wechat_api import WechatCgiApi
from lazyplant.models import IoTRecord

#wechat = WechatBasic(token=settings.WECHAT_TOKEN, appid=settings.WECHAT_ACCOUNT)

# Create your views here.
@csrf_exempt
def smart_entry(request):
    signature = request.REQUEST.get('signature', None)
    timestamp = request.REQUEST.get('timestamp', None)
    nonce = request.REQUEST.get('nonce', None)

    # if it's account authenticate request
    echostr = request.REQUEST.get('echostr', None)
    if echostr:
        return HttpResponse(echostr)

    wechat = WechatBasic(token=settings.WECHAT_TOKEN, appid=settings.WECHAT_ACCOUNT)

    # 对签名进行校验
    if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        # 对 XML 数据进行解析 (必要, 否则不可执行 response_text, response_image 等操作)
        body_text = request.body
        log.info("Wechat message come: {0}".format(body_text))

        wechat.parse_data(body_text)
        # 获得解析结果, message 为 WechatMessage 对象 (wechat_sdk.messages中定义)
        message = wechat.get_message()

        #response = None
        if isinstance(message, EventMessage):
            if message.type == 'click' and message.key == 'V1001_PLANT_LIVE':
                # post latest image
                records = IoTRecord.objects.filter().order_by("-timestamp")[:1]
                if not records or not records[0].image:
                    return HttpResponse(wechat.response_text(u"找不到你的菜呀！"))

                api = WechatCgiApi(app_id=settings.WECHAT_APP_ID, app_secret=settings.WECHAT_APP_SECRET)
                result_token = WechatConfig.objects.filter(key=WechatConfig.KEY_ACCESS_TOKEN)
                if not result_token or result_token[0].is_expired():
                    result_update, resp_json = WechatConfig.refresh_access_token()
                    if result_update:
                        token = resp_json[u"access_token"]
                    else:
                        log.error("Cannot update wechat access token: {0}".format(resp_json))
                        return HttpResponse(wechat.response_text(u"服务器有点小问题。。。"))
                        
                else:
                    token = result_token[0].value

                with open(records[0].image.path, 'rb') as live_image:
                    api_result = api.create_temp_media(token, "image", media={"media": live_image})
                    log.info("Wechat upload image response: {0}".format(api_result))
                    if api_result and api_result["media_id"]:
                        return HttpResponse(wechat.response_image(api_result["media_id"]))
                    else:
                        log.warning("Wechat upload temporary image failed: {0}".format(api_result))
                        return HttpResponse(wechat.response_text(u"发送图片失败: {0}".format(str(api_result))))


            elif message.type == 'click' and message.key == 'V1001_HEALTH_STATS':
                return HttpResponse(wechat.response_text(u"功能未实现"))

            elif message.type == 'click' and message.key == 'V1001_GROW_VID':
                return HttpResponse(wechat.response_text(u"功能未实现。"))

            elif message.type == 'click' and message.key == 'V1001_PLAY_CUTE':
                return HttpResponse(wechat.response_text(u"我已经长得很好吃了，主人请摘我吧！"))

        #    response = wechat.response_text(content=u'文字信息')

        response = wechat.response_news([{
                "title": "我是别人的菜",
                "description": "你要的功能失败了，这是测试页面",
                "picurl": "http://wechat.lucki.cn/static/iotimages/test.jpg",
                "url": "http://wechat.lucki.cn/",
            },])

        return HttpResponse(response)

    return HttpResponse("Not implemented yet")



