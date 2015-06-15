from django.contrib import admin
from .models import IoTRecord
from django.contrib.staticfiles.templatetags.staticfiles import static

# Register your models here.

class IoTRecordModelAdmin(admin.ModelAdmin):
    list_display = ["co2", "o2", "humidity", "temperature", "timestamp", "live_image"]

    def live_image(self, obj):
        if obj and obj.image:
            return "<img src='{0}' style='width:200px;height:auto;'>".format(static(obj.image))
        else:
            return "None"
    live_image.allow_tags = True


admin.site.register(IoTRecord, IoTRecordModelAdmin)


