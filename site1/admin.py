from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate

# Permissions
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Signals
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from site1.models import *
from site1.ami_reboot import *
#
#	Users pre_save hook
#
@receiver(pre_save, sender = User)
def set_user_rights(instance, **kwargs):
	# make all created users access to admin site
	instance.is_staff = True

	# to avoide self blocking
	if instance.is_superuser:
		instance.is_active = True

	return instance


# deleting configs
@receiver(pre_delete, sender = device)
def delete_config(instance, **kwargs):
	delete_sip_conf(instance.mac_address)
	return instance

#
#	Users post_save hook
#
#@receiver(post_save, sender = User)
def set_user_rights_postsave(sender, instance, created, **kwargs):
	print "sender", sender
	print "instance", instance
	instance.groups.add(Group.objects.get(name='devices_rwd'))
	print instance.groups

#
# hiding Group from admin
#
admin.site.unregister(Group)


#
#  Reboot selected devises
#
def ata_reboot(modeladmin, request, queryset):
	ami = AMI_reboot_device()
	ata_reboot.short_description = "Reboot selected devices"
	for i in queryset:
		ami.put_data(i.sip_msg_user)
	return


#  "Generate config for selected devices"
def ata_config(modeladmin, request, queryset):
	ata_config.short_description = "Generate config for selected devices"
	for i in queryset:
		i.version = i.version + 1
		i.save()
		arr1 = {}
		arr2 = {}
		arr1['path']		= i.organization.tftp_dir
		print arr1['path']
		arr1['mac'] 		= i.mac_address
		arr2['version']		= str(i.version)
		arr2['voip1_user']	= i.sip_user
		arr2['voip1_password']	 = i.sip_password
		arr2['voip1_phonenumber']= i.phone_number
		arr2['voip2_user']		 = i.sip_msg_user
		arr2['voip2_password']	 = i.sip_msg_password
		# arr2['voip1_rule1_pattern'] = i.voip1_rule1_pattern
		arr2['voip1_rule1_prefix'] = i.voip1_rule1_prefix
		arr2['voip1_rule1_offset'] = i.voip1_rule1_offset
		arr2['voip1_rule1_length'] = i.voip1_rule1_length
		arr2['voip1_rule1_suffix'] = i.voip1_rule1_suffix
		arr2['voip1_rule1_callerid'] = i.voip1_rule1_callerid
		arr2['voip1_protocol'] = i.voip1_protocol
		arr2['voip1_host'] = i.sip_server

		#arr2['voip1_rule2_pattern'] = i.voip1_rule2_pattern
		#arr2['voip1_rule2_prefix'] = i.voip1_rule2_prefix
		#arr2['voip1_rule2_offset'] = i.voip1_rule2_offset
		#arr2['voip1_rule2_length'] = i.voip1_rule2_length
		#arr2['voip1_rule2_suffix'] = i.voip1_rule2_suffix
		tmp = ConfigMake()
		tmp.prepare_data(arr1, arr2)
	return

# generate config for sertain device
def ata_config2(i):
	i.version = i.version + 1
	i.save()
	arr1 = {}
	arr2 = {}
	arr1['path']		= i.organization.tftp_dir
	print arr1['path']
	arr1['mac'] 		= i.mac_address
	arr2['version']		= str(i.version)
	arr2['voip1_user']	= i.sip_user
	arr2['voip1_password']	 = i.sip_password
	arr2['voip1_phonenumber']= i.phone_number
	arr2['voip2_user']		 = i.sip_msg_user
	arr2['voip2_password']	 = i.sip_msg_password
	# arr2['voip1_rule1_pattern'] = i.voip1_rule1_pattern
	arr2['voip1_rule1_prefix'] = i.voip1_rule1_prefix
	arr2['voip1_rule1_offset'] = i.voip1_rule1_offset
	arr2['voip1_rule1_length'] = i.voip1_rule1_length
	arr2['voip1_rule1_suffix'] = i.voip1_rule1_suffix
	arr2['voip1_rule1_callerid'] = i.voip1_rule1_callerid
	arr2['voip1_protocol'] = i.voip1_protocol
	arr2['voip1_host'] = i.sip_server

	#arr2['voip1_rule2_pattern'] = i.voip1_rule2_pattern
	#arr2['voip1_rule2_prefix'] = i.voip1_rule2_prefix
	#arr2['voip1_rule2_offset'] = i.voip1_rule2_offset
	#arr2['voip1_rule2_length'] = i.voip1_rule2_length
	#arr2['voip1_rule2_suffix'] = i.voip1_rule2_suffix
	tmp = ConfigMake()
	tmp.prepare_data(arr1, arr2)
	return


#inline device history
#TabularInline, StackedInline
class DeviceHistoryInline(admin.TabularInline):
	model = DeviceHistory

	readonly_fields = ('device', 'last_connection', 'inet_type',
		'signal_strenght', 'sip_voip_registered', 'sip_control_registered')

	can_delete = False
	#number of rows to show after last value.
	extra = 0
	ordering = ("-last_connection",)

#
# customising device admin view
#
class DevicesAdmin(admin.ModelAdmin):

	# Customize what to see in edit form
	def get_form(self, request, obj=None, **kwargs):
		if request.user.is_superuser:
#			self.exclude = None
			self.readonly_fields = ('last_connection','inet_type','signal_strenght', 'sip_voip_registered', 'sip_control_registered',
									'sip_msg_user','sip_msg_server','sip_msg_password','voip1_protocol')
			self.fieldsets = (
								( None, {'fields': (('mac_address', 'organization'),)} ),
								( 'Customer info',
										{
										'fields':(
													'customer_no',
													('customer_fname','customer_lname'),
													('customer_zip','customer_city'),
													'customer_address',
													)
										}
								),
								( 'VoIP SIP acccount',
										{
										'fields':(
												'sip_server',
												('sip_user','sip_password'),
												'phone_number',
												)
										}
								),
								( 'VoIP Dial plan1',
									{
										'classes': ('collapse',),
										'fields':(
													'voip1_protocol',
													('voip1_rule1_prefix'),
													('voip1_rule1_offset','voip1_rule1_length'),
													('voip1_rule1_suffix', 'voip1_rule1_callerid')
												)
									}
								),
								( 'SIP Managment acccount',
									{
										'classes': ('collapse',),
										'fields':(
													'sip_msg_server',
													('sip_msg_user','sip_msg_password'),
												)
									}
								),
								( 'SIM card info',
									{
										'classes': ('collapse',),
										'fields':(
													'sim_card_number',
													'sim_card_carrier',
												)
									}
								),

								( 'Device state',
									{
										'fields':(
													'last_connection', 'inet_type','signal_strenght',
													'sip_voip_registered', 'sip_control_registered'
												)
									}
								),
							)

		else:
#			self.exclude = ['organization']
			self.readonly_fields = ('last_connection','inet_type','signal_strenght', 'sip_voip_registered', 'sip_control_registered','organization','voip1_protocol')
			self.fieldsets = (
								( None, {'fields': (('mac_address', 'organization'),)} ),
								( 'Customer info',
										{
										'fields':(
													'customer_no',
													('customer_fname','customer_lname'),
													('customer_zip','customer_city'),
													'customer_address',
													)
										}
								),
								( 'SIP acccount',
										{
										'fields':(
												'sip_server',
												('sip_user','sip_password'),
												'phone_number',
												)
										}
								),
								( 'SIM card info',
									{
										'classes': ('collapse',),
										'fields':(
													'sim_card_number',
													'sim_card_carrier',
												)
									}
								),

								( 'Device state',
									{
										'fields':(
													'last_connection', 'inet_type','signal_strenght',
													'sip_voip_registered', 'sip_control_registered'
												)
									}
								),
							)

		return super(DevicesAdmin, self).get_form(request, obj, **kwargs)


	# what to show in list view
	list_display = ('mac_address','customer_fname','customer_lname',
					'last_connection','signal_strenght','inet_type',
					)


	# Group_by filter
	list_filter = ('signal_strenght','inet_type','last_connection', 'sip_control_registered', 'sip_voip_registered')

	# Search fields
	search_fields = ['mac_address','customer_fname','customer_lname']

	# adding custom action
	actions = [ata_reboot, ata_config]

	# If current user=superuser => show all data
	# else show only with devices.organization = current_user.organization
	def get_queryset(self, request):
		qs = super(DevicesAdmin, self).get_queryset(request)

		if request.user.is_superuser:
			return qs
		else:
			user = Employee.objects.get(user=request.user)
			return qs.filter(organization=user.organization)
	#
	# trick for getting current_user in pre_save hook and set
	# devices.organization = current_user.organization
 	#
	def save_model( self, request, obj, form, change ):
		#pre save stuff here

		# auto set organization for simple users
		if not request.user.is_superuser:
			obj.organization = Employee.objects.get(user=request.user).organization

		# set value for voip1_protocol
		obj.voip1_protocol=organization.objects.get(name=obj.organization).voip1_protocol
		#print organization.objects.get(name=obj.organization)

		# empty or default messages password -> autogenerate
		if (not obj.sip_msg_password) or (obj.sip_msg_password is EMPTY_PASSWORD):
			obj.sip_msg_password = random_passwd()

		obj.mac_address = obj.mac_address.lower()
		# generate username for messages
		obj.sip_msg_user = obj.mac_address

		#saving now
		obj.save()

		#post save stuff here
		# create sip config files for Asterisk
		write_sip_conf(obj.mac_address, obj.sip_msg_user, obj.sip_msg_password)

		#updating autoprovision file for devices (it duplicates dropbox action)
		ata_config2(obj)
		#post save stuff here

	#add inlines
	inlines = [ DeviceHistoryInline, ]

admin.site.register(device, DevicesAdmin)


#
# customising organization admin
#
class OrganizationAdmin(admin.ModelAdmin):
	list_display = ['name', 'api_key', 'voip1_protocol']

	# trick for generate API_KEY
	def save_model( self, request, obj, form, change ):
		#pre save stuff here

		#	 empty or default messages password -> autogenerate
		if (not obj.api_key) or (obj.api_key == EMPTY_PASSWORD):
				obj.api_key = random_passwd()

		#saving now
		obj.save()

  		#post save stuff here


admin.site.register(organization, OrganizationAdmin)

#
# customising user admin
#
class EmployeeInline(admin.StackedInline):
	model = Employee
	can_delete = False
	verbose_name_plural = 'employee'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
	inlines = (EmployeeInline, )
	fieldsets = (
			(None, {'fields': ('username', 'password', 'first_name','last_name','groups','is_active',)}),
			)
	list_display = ('username', 'first_name', 'last_name', 'last_login', 'is_active',)



# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


#
# hook for user login. Usefull for logging
#
@receiver(user_logged_in, sender = User)
def DevicesAdmin_presave(request, **kwargs):
	pass




##admin.site.register(DeviceHistory)
