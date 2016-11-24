# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from site1.models import *
from site1.admin import ata_config2
from site1.ami_reboot import *

import datetime
import pytz
import json
from django.http import JsonResponse

def api_sip(request, arg_mac, arg_2, arg_3):


	if arg_2 in 'voip' or arg_2 in 'control':

		try:
			item = device.objects.get(mac_address=arg_mac)
		except:
			test = "Object not found. MAC=%s" % (arg_mac)
			return render_to_response('test.html', locals(),RequestContext(request))


		if arg_2 in 'voip':

			item.sip_voip_registered=int(arg_3)
		else:
			item.sip_control_registered=int(arg_3)
			pass
		item.last_connection = datetime.datetime.now()
		item.save()
		update_history(item)

	test = "%s:%s:%s:" % (arg_mac, arg_2, arg_3)
	return render_to_response('test.html', locals(),RequestContext(request))

def api_cell(request, arg_mac, arg_2):
	if arg_2 in 'normal' or arg_2 in 'poor' or arg_2 in 'good' :
		try:
			item = device.objects.get(mac_address=arg_mac)
		except:
			test = "Object not found. MAC=%s" % (arg_mac)
			return render_to_response('test.html', locals(),RequestContext(request))

		item.signal_strenght =arg_2
		item.last_connection = datetime.datetime.now()
		item.save()
		update_history(item)

	test = "%s: %s " % (arg_mac, arg_2)
	return render_to_response('test.html', locals(),RequestContext(request))

def api_inet(request, arg_mac, arg_2):
	if arg_2 in 'cellular' or arg_2 in 'wan':
		try:
			item = device.objects.get(mac_address=arg_mac)
		except:
			test = "Object not found. MAC=%s" % (arg_mac)
			return render_to_response('test.html', locals(),RequestContext(request))

		item.inet_type = arg_2
		item.last_connection = datetime.datetime.now()
		item.save()
		update_history(item)
	test = "%s:%s " % (arg_mac, arg_2)
	return render_to_response('test.html', locals(),RequestContext(request))

def update_history(arg_device):
	tmp = DeviceHistory(device=arg_device)
	tmp.last_connection = datetime.datetime.now()
	tmp.inet_type		= arg_device.inet_type
	tmp.signal_strenght = arg_device.signal_strenght
	tmp.sip_voip_registered = arg_device.sip_voip_registered
	tmp.sip_control_registered = arg_device.sip_control_registered
	tmp.save()
	
	#delete old items
	items_to_left = 6
	
	items_to_delete = DeviceHistory.objects.filter(device=arg_device).order_by('-last_connection')[items_to_left:]
	
	for i in items_to_delete:
		i.delete()
		

	
#needed for CERT installation
def ssl(request):

	test = 'WjbzeYCe'
	return render_to_response('emply.html', locals())
#
#  API2. get state of device
#
def api2_state(request,arg_api_key, arg_mac=None):
	js_data = {"api_key":arg_api_key, "date" : str(datetime.datetime.now()) }

	# we have no MAC => get all data
	if arg_mac:
		try:
			item = device.objects.filter(organization=organization.objects.get(api_key=arg_api_key), mac_address=arg_mac)
		except:
			js_data.update({"status" : "ERROR: Object not found"})

	# certain device
	else:
		try:
			item = device.objects.filter(organization=organization.objects.get(api_key=arg_api_key))
		except:
			js_data.update({"status" : "ERROR: Object not found"})


	#generate json body
	result = []
	try:
		for i in item:
			result.append({
							 "mac_address":i.mac_address,
							 "sip_voip_registered": i.sip_voip_registered,
							 "sip_control_registered": i.sip_control_registered,
							 "last_connection": str(i.last_connection),
							 "phone_number": i.phone_number,
							 "customer_fname": i.customer_fname,
							 "customer_lname": i.customer_lname,
							 "inet_type": i.inet_type,
							 "signal_strenght": i.signal_strenght
						})
		js_data.update({"data":result})

	except:
		pass

# for production
	return JsonResponse(js_data)

	# for debugging
	#json_response = json.dumps(js_data,sort_keys=True,indent=4)
	#return render_to_response('json.html', locals())
#
#  API2. create a new device
#
def api2_new_device(request,arg_api_key):
	js_data = {"api_key":arg_api_key, "date" : str(datetime.datetime.now()) }

	if request.method == 'POST':

		# check that device not exists
		try:
			item = device.objects.get(mac_address=request.POST['mac_address'])
		except:
			item = None
			pass

		# device already exists. generate error
		if item:
			js_data.update({'status':'ERROR:item alreay exists', 'mac_address':request.POST['mac_address']})

		# if item not exists -> create item
		else:

			tmp = device(mac_address = request.POST['mac_address'])

			tmp.mac_address 	= request.POST['mac_address'].lower()
			tmp.organization =  organization.objects.get(api_key=arg_api_key)
			tmp.sip_user 	= request.POST['sip_user']
			tmp.sip_password = request.POST['sip_password']
			tmp.phone_number = request.POST['phone_number']
			tmp.customer_no 	= request.POST['customer_no']
			tmp.customer_fname = request.POST['customer_fname']
			tmp.customer_lname = request.POST['customer_lname']
			tmp.customer_address 	= request.POST['customer_address']
			tmp.customer_zip 		= request.POST['customer_zip']
			tmp.customer_city 		= request.POST['customer_city']
			tmp.sip_msg_password = random_passwd()

			# generate username for messages
			tmp.sip_msg_user = tmp.mac_address

			tmp.save()
			#generate config for it after save item in DB
			ata_config2(tmp)

			# create sip config files for Asterisk
			write_sip_conf(tmp.mac_address, tmp.sip_msg_user, tmp.sip_msg_password)


			js_data.update({"status":'OK:item created', 'mac_address':request.POST['mac_address']})

#	json_response = json.dumps(js_data,sort_keys=True,indent=4)
	#return render_to_response('json.html', locals())
	return JsonResponse(js_data)
#
#  API2. reboot a new device
#
def api2_reboot(request,arg_api_key, arg_mac):

	js_data = {"api_key":arg_api_key, "date" : str(datetime.datetime.now()), 'mac_address':arg_mac}

	ami = AMI_reboot_device()

	try:
		item = device.objects.get(organization=organization.objects.get(api_key=arg_api_key), mac_address=arg_mac)

		# put device in Redis query
		ami.put_data(item.sip_msg_user)
		js_data.update({"status" : "OK. Object has been placed in reboot query"})

	except:
		js_data.update({"status" : "Object not found"})


#	json_response = json.dumps(js_data,sort_keys=True,indent=4)
#	return render_to_response('json.html', locals())
	return JsonResponse(js_data)

#
#  API2. update devices data from customer side
#
def api2_update(request,arg_api_key, arg_mac):



	js_data = {"api_key":arg_api_key, "date" : str(datetime.datetime.now()), 'mac_address':arg_mac}
	EDITABLE_FIELDS = [
						'sip_server',
						'sip_user',
						'sip_password',
						'phone_number',
						'customer_no',
						'customer_fname',
						'customer_lname',
						'customer_address',
						'customer_zip',
						'customer_city'
						]

	try:
		item = device.objects.get(organization=organization.objects.get(api_key=arg_api_key), mac_address=arg_mac)
		js_data.update({"status" : "OK"})

	except:
		js_data.update({"status" : "Object not found"})
		item = None

	updated_fields = []

	# if device exists
	if item and request.method == 'POST' and len (request.POST):

		# cycle through fields we allow to change
		for i in EDITABLE_FIELDS:
				# check that this field was in POST
				if i in request.POST:
					item.__dict__[i] = request.POST[i]
					updated_fields.append({i:request.POST[i]})


		# save changes
		item.save()

	js_data.update({'updated_fields':updated_fields})

#	json_response = json.dumps(js_data,sort_keys=True,indent=4)
#	return render_to_response('json.html', locals())
	return JsonResponse(js_data)

#	
#
#  API. update devices status from box side
#
def api_update(request, arg_mac):



	js_data = {"date" : str(datetime.datetime.now()), 'mac_address':arg_mac}
	EDITABLE_FIELDS = [
						'inet_type',
						'signal_strenght',
						'sip_voip_registered',
						'sip_control_registered'
						]

	try:
		item = device.objects.get(mac_address=arg_mac)
		js_data.update({"status" : "OK"})

	except:
		js_data.update({"status" : "Object not found"})
		item = None

	updated_fields = []

	# if device exists
	if item and request.method == 'POST' and len (request.POST):

		# cycle through fields we allow to change
		for i in EDITABLE_FIELDS:
				# check that this field was in POST
				if i in request.POST:
					item.__dict__[i] = request.POST[i]
					updated_fields.append({i:request.POST[i]})

		item.last_connection = datetime.datetime.now()
		# save changes
		item.save()
		update_history(item)

	js_data.update({'updated_fields':updated_fields})
	
	return JsonResponse(js_data)

