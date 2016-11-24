# -*- coding: utf-8 -*-

from django import forms

class ATA_box_Form(forms.Form):
	id = forms.CharField(widget=forms.HiddenInput(), required=False)
	phone 	= forms.CharField(label='Phone Number', max_length=11,required=False)
	mac 	= forms.CharField(label='MAC address', max_length=12,required=True)
	sip_voice 	= forms.CharField(label='SIP registration number for Voice', max_length=5,required=False)
	sip_control	= forms.CharField(label='SIP registration number for Control', max_length=5,required=False)
