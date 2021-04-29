from django import forms
    
class DeviceForm(forms.Form):
    hostname = forms.CharField(required=False)
    ip = forms.CharField()
    mac = forms.CharField()
    ports = forms.CharField(required=False)
    ipSwitch = forms.BooleanField(required=False)
    firmware = forms.CharField(required=False)
    vendor = forms.CharField(required=False)
    deviceType = forms.CharField(required=False)
    deviceStatus = forms.BooleanField()

class UpdateForm(forms.Form):
    mac = forms.CharField()
    last_update = forms.CharField()
    firmware = forms.CharField()
