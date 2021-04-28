from django import forms
    
class DeviceForm(forms.Form):
    hostname = forms.CharField(required=False)
    ip = forms.CharField()
    mac = forms.CharField()
    ports = forms.CharField()
    ipSwitch = forms.BooleanField()
    firmware = forms.CharField()
    vendor = forms.CharField()
    deviceStatus = forms.BooleanField()
