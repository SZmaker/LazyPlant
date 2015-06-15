# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from wechat_sdk import WechatBasic
from wechat_sdk.messages import (
    TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage
)


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
        wechat.parse_data(body_text)
        # 获得解析结果, message 为 WechatMessage 对象 (wechat_sdk.messages中定义)
        message = wechat.get_message()

        #response = None
        #if isinstance(message, TextMessage):
        #    response = wechat.response_text(content=u'文字信息')

        response = wechat.response_news([{
                "title": "图文信息怎么样？",
                "description": "我就试试种菜的图文信息行不行",
                "picurl": "http://wechat.lucki.cn/static/iotimages/test.jpg",
                "url": "http://wechat.lucki.cn/admin/",
            },])

        return HttpResponse(response)

    return HttpResponse("Not implemented yet")



