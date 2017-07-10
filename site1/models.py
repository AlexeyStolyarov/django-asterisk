from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import random
import string
EMPTY_PASSWORD = '**autogeneration**'

def random_passwd():
	return ''.join([random.choice(string.ascii_letters + string.digits) for x in range(10)])
class organization(models.Model):
	name				= models.CharField(max_length=20,blank=False,null=False)
	tftp_dir			= models.CharField(max_length=30,blank=False,null=False)
	api_key				= models.CharField(max_length=30,blank=False,null=False,default=EMPTY_PASSWORD)
	voip1_protocol 		= models.CharField(max_length=30,blank=False,null=False,default='' )
	def __unicode__(self):
		return u'%s' % (self.name)


class device(models.Model):
	organization		= models.ForeignKey(organization,related_name='organization')

	mac_address		= models.CharField(max_length=12,blank=False,null=False)
	lock_internet		= models.BooleanField(default=True)
	last_connection		= models.DateTimeField(blank=True,null=True)
	sip_server		= models.CharField(max_length=30,blank=False,null=False, default='sip.phone.suissephone.ch')
	sip_user		= models.CharField(max_length=30,blank=False,null=False)
	sip_password		= models.CharField(max_length=30,blank=False,null=False)
	phone_number		= models.CharField(max_length=30,blank=True,null=True)
	customer_no		= models.CharField(max_length=30,blank=False,null=False)
	customer_fname		= models.CharField(max_length=30,blank=False,null=False,verbose_name='Customer First name')
	customer_lname		= models.CharField(max_length=30,blank=False,null=False,verbose_name='Customer Second name')
	customer_address	= models.CharField(max_length=40,blank=False,null=False)
	customer_zip		= models.CharField(max_length=30,blank=False,null=False)
	customer_city		= models.CharField(max_length=12,blank=False,null=False)
	sip_msg_server		= models.CharField(max_length=30,blank=False,null=False, default='ata.sipstar.ch')
	sip_msg_user		= models.CharField(max_length=30,blank=False,null=False,default=EMPTY_PASSWORD)
	sip_msg_password	= models.CharField(max_length=30,blank=True,null=True,default=EMPTY_PASSWORD)
	inet_type			= models.CharField(max_length=12,blank=True,null=True)
	signal_strenght		= models.CharField(max_length=12,blank=True,null=True)
	voip1_protocol 		= models.CharField(max_length=25,blank=True,null=True, default='[configured via organization]')
	sip_voip_registered	= models.CharField(max_length=6,blank=True,null=True, verbose_name='Registered on VoIP server')
	sip_control_registered	= models.CharField(max_length=6,blank=True,null=True, verbose_name='Registered on managment server')
	#voip1_rule1_pattern = models.CharField(max_length=12,blank=True,null=True,default="_0X.")
	voip1_rule1_prefix  = models.CharField(max_length=12,blank=True,null=True,default="")
	voip1_rule1_offset  = models.CharField(max_length=12,blank=True,null=True,default="")
	voip1_rule1_length  = models.CharField(max_length=12,blank=True,null=True,default="")
	voip1_rule1_suffix  = models.CharField(max_length=12,blank=True,null=True,default="")
	voip1_rule1_callerid = models.CharField(max_length=12,blank=True,null=True,default="")
	# voip1_rule2_pattern  = models.CharField(max_length=12,blank=True,null=True,default="_8.")
	# voip1_rule2_prefix   = models.CharField(max_length=12,blank=True,null=True,default="1")
	# voip1_rule2_offset   = models.CharField(max_length=12,blank=True,null=True,default="'1'")
	# voip1_rule2_length   = models.CharField(max_length=12,blank=True,null=True,default="'1'")
	# voip1_rule2_suffix   = models.CharField(max_length=12,blank=True,null=True,default="'1'")

	sim_card_number = models.CharField(max_length=22,blank=True,null=True,default="")
	sim_card_carrier = models.CharField(max_length=22,blank=True,null=True,default="")

	version			= models.IntegerField(default=1)
	#last_registration
	def __unicode__(self):
		return u'%s' % (self.mac_address)


class Employee(models.Model):
	user 				= models.OneToOneField(User, on_delete=models.CASCADE)
	organization		= models.ForeignKey(organization)
	def __unicode__(self):
		return u'%s %s' % (self.user.first_name, self.user.last_name)


class DeviceHistory(models.Model):
	device				= models.ForeignKey(device)
	last_connection		= models.DateTimeField(blank=True,null=True)
	inet_type			= models.CharField(max_length=12,blank=True,null=True)
	signal_strenght		= models.CharField(max_length=12,blank=True,null=True)
	sip_voip_registered	= models.CharField(max_length=6,blank=True,null=True, verbose_name='Registered on VoIP server')
	sip_control_registered	= models.CharField(max_length=6,blank=True,null=True, verbose_name='Registered on managment server')
