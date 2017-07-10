#!/usr/bin/env python

"""
"""

import asterisk.manager
import sys
import os
import redis
import time
import pickle
import base64


AMI_LOGIN='admin'
AMI_PASSWD='****'
#help (asterisk.manager)


# ==============================================================================
#
# write sip configuration for ata boxes
#
def write_sip_conf(mac_address, sip_msg_user, sip_msg_password):
	f = open("/srv/sip_conf/%s.conf" % (mac_address), 'w')
	f.write("[%s]\n" % (sip_msg_user))
	f.write("type=friend\n")
	f.write("qualify=yes\n")
	f.write("host=dynamic\n")
	f.write("insecure=invite,port\n")
	f.write("canreinvite=no\n")
        f.write("context=messages\n")

	f.write("defaultuser=%s\n" % (sip_msg_user))
	f.write("secret=%s\n" % (sip_msg_password))
	f.close()

	print "[%s]: config /srv/sip_conf/%s.conf has been created" %  (time.strftime("%d %b %Y, %H:%m"), mac_address )


def delete_sip_conf(mac_address):
	try:
		os.remove("/srv/sip_conf/%s.conf" % (mac_address) )
	except:
		pass


# ==============================================================================


#
#  create autoprovision file for devises
#

class ConfigMake:
	path		= ''
	mac		= ''
	fields		= {}
	fields2		= {}
	file_extens	= ".conf"
	path_refix	= "/srv/tftp"

	_fields		= ['internet', 'voip1_enable', 'voip1_protocol', 'voip1_host',
			    'voip1_user', 'voip1_password','voip1_phonenumber', 'voip1_rule1_pattern',
			    'voip1_rule1_prefix', 'voip1_rule1_offset', 'voip1_rule1_length',
			    'voip1_rule1_suffix', 'voip1_rule1_protocol', 'voip1_rule1_callerid',
			    'voip1_rule2_pattern',   'voip1_rule2_prefix', 'voip1_rule2_offset',
			    'voip1_rule2_length', 'voip1_rule2_suffix', 'voip1_rule2_callerid',
			    'voip1_rule2_protocol', 'voip2_enable', 'voip2_host', 'voip2_user',
			    'voip2_password', 'voip2_protocol']


	redis 		= redis.StrictRedis(host='localhost', port=6379, db=0)
	r_pubsub	= None


	def __init__(self):
		self.fill_vars()

		self.r_pubsub = self.redis.pubsub()
		self.r_pubsub.psubscribe('config',)
		# skip first crap message
		self.r_pubsub.get_message()

	def fill_vars(self):
		# devault values
#		self.fields["version"]  			= "1.2"
		self.fields["internet"]  			= "cellular"
		self.fields["voip1_enable"]  		= "1"
		###self.fields["voip1_protocol"]  		= "'suissephone'"
		### self.fields["voip1_host"]  			= "'Sip.phone.suissephone.ch'"
		self.fields["voip1_rule1_pattern"]	= "_0X."
		#self.fields["voip1_rule1_prefix"]  	= ""
		#self.fields["voip1_rule1_offset"]  	= "'1'"
		#self.fields["voip1_rule1_length"]  	= "'1'"
		#self.fields["voip1_rule1_suffix"]  	= "'1'"
		self.fields["voip1_rule1_protocol"]	= "'SIP'"
		self.fields["voip1_rule1_callerid"]	= "'globacom'"
		self.fields["voip1_rule2_pattern"]	= "_1X."
		#self.fields["voip1_rule2_prefix"]	= "1"
		#self.fields["voip1_rule2_offset"]	= "'1'"
		#self.fields["voip1_rule2_length"]	= "'1'"
		#self.fields["voip1_rule2_suffix"]	= "'1'"
		#self.fields["voip1_rule2_callerid"]	= "'dragino1'"
		#self.fields["voip1_rule2_protocol"]	= "'SIP'"
		self.fields["voip2_enable"]  		= "1"
		self.fields["voip2_protocol"]  		= "globacom"
		self.fields["voip2_host"]			= "ata.sipstar.ch"
		self.fields["update_voip"]		= "1"
		self.fields["update_network"]		= "1"
		self.fields["package_link1"]		= "'http://www.dragino.com/downloads/odm/bb-iot-pkg/gbc/dragino/'"
		self.fields["update_pkg_maintain"]	= "1"



	test = {}
	test2 = {}
	test['path']='/test33'
	test['mac'] ='99922255533'

	test2['voip1_user']='user1'
	test2['voip1_password']='passwd1'
	test2['voip1_phonenumber']='phone'
	test2['voip2_user']='iser2'
	test2['voip2_password']='pass2'

	def prepare_data(self, arg1, arg2):

		tmp = base64.encodestring(pickle.dumps((arg1,arg2), pickle.HIGHEST_PROTOCOL))
		self.redis.publish('config', tmp)
#		print tmp


	def read_data(self):
		tmp = None
		tmp =  self.r_pubsub.get_message()
		arr = {}
		arr2 = {}
		if tmp:
			try:
	    			arr, arr2  =  pickle.loads(base64.decodestring(tmp['data']))
				self.path 	= arr['path']
				self.mac	= arr['mac']
				self.fields2	= arr2
				return True
			except:
				return
		else:
			return


	def write_config(self):

#		full_path	= self.path_refix +  self.path
		full_path	= self.path_refix
		full_fn		= "%s/%s%s" % (full_path, self.mac, self.file_extens)

		if not os.path.exists(full_path):
			os.makedirs(full_path)
		f = open(full_fn, 'w')
		for i in self.fields:
			f.write(i+"="+ self.fields[i]+"\n")

		for i in self.fields2:
			try:
				f.write(i+"="+ self.fields2[i]+"\n")
			except:
				pass
				
		f.close()

		print "[%s]: config %s has been created" %  (time.strftime("%d %b %Y, %H:%m"), full_fn )




# ===============================================================================

#
# asterisk AMI interface to recieve commands via REDIS/messages and give commands to reboot boxes
# via AMI/messages
# Redis/messages is used for do it asyncronous

class AMI_reboot_device:

	manager = asterisk.manager.Manager()
	redis = redis.StrictRedis(host='localhost', port=6379, db=0)
	r_pubsub = None

	def __init__(self):

		self.r_pubsub = self.redis.pubsub()
		self.r_pubsub.psubscribe('my-*',)
		# skip first crap message
		self.r_pubsub.get_message()


	def connect(self,arg_user, arg_passwd):

		# connect to the manager
		try:

			self.manager.connect('localhost')
			self.manager.login(arg_user, arg_passwd)
			# get a status report
			response = self.manager.status()
			#print(response)
		except asterisk.manager.ManagerSocketException as e:
			#
			print "Error connecting to the manager: %s" % e.strerror
			sys.exit(1)
		except asterisk.manager.ManagerAuthException as e:
			print "Error logging in to the manager: %s" % e.strerror
			sys.exit(1)
		except asterisk.manager.ManagerException as e:
			print "Error: %s" % e.strerror
			sys.exit(1)

		finally:
			# remember to clean up
			pass

	def reboot_device(self, arg_dev_id):

		cdict = {"Action": "MessageSend",
				"ActionID": "value",
				"To": "sip:"+arg_dev_id,
				"From": "sip:"+arg_dev_id,
				"Body": "reboot"}
		#print(cdict)
		response = self.manager.send_action(cdict)
		# print(response.data)
		print "[%s]: %s has been rebooted" %  (time.strftime("%d %b %Y, %H:%m"),arg_dev_id )


	def close(self):
		self.manager.logoff()
		self.manager.close()
		self.file.close()
		print "bye!"

	def read_data(self):
		tmp = None
		tmp =  self.r_pubsub.get_message()
		if tmp:
			return tmp['data']
		else:
			return

	def put_data(self, arg):
		self.redis.publish('my-channel', arg)



if __name__ == '__main__':
	ami = AMI_reboot_device()
	ami.connect(AMI_LOGIN, AMI_PASSWD)
	conf = ConfigMake()

	while True:
		x = ami.read_data() or None
		if x:
		    ami.reboot_device(str(x))

		z = conf.read_data() or None
		if z:
			conf.write_config()

		time.sleep(1)  # be nice to the system :)
	ami.close()
