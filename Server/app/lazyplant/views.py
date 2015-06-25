from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import IoTRecord
from .forms import IoTDataForm

# Create your views here.
@csrf_exempt
def upload_iot(request):
    if request.method == "POST":
        form = IoTDataForm(request.POST)
        if form.is_valid():
            record, created = IoTRecord.objects.get_or_create(timestamp=timezone.now())
            record.co2 = form.cleaned_data["co2"]
            record.o2 = form.cleaned_data["o2"]
            record.humidity = form.cleaned_data["humidity"]
            record.temperature = form.cleaned_data["temperature"]
            if request.FILES and request.FILES["image"]:
                record.image = request.FILES["image"]

            record.save()

            return HttpResponse("OK")

        else:
            print(form.errors)

    return HttpResponse("No data\n")


def myplant(request):
    return HttpResponse("Your plant is looking good!")

def myplant_vid(request):
    return HttpResponse("Your plant's growing video!")
