from django import forms

# Create your tests here.
class IoTDataForm(forms.Form):
    co2 = forms.FloatField(required=False)
    o2 = forms.FloatField(required=False)
    humidity = forms.FloatField(required=False)
    temperature = forms.FloatField(required=False)
    image = forms.ImageField(required=False)
    timestamp = forms.DateTimeField()

