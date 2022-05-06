from itertools import filterfalse
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


Group = (
		('Agricultural/Livestock,Fisheries Producer’s Group','Agricultural/Livestock/Fisheries Producer’s Group (including marketing groups)'), 
	 	('Water Users’ Group', 'Water Users’ Group'),
		('Credit or Microfinance Group','Credit or Microfinance Group (including SACCOs/merry-go-rounds/ VSLAs)'),
		('Other','Other [Women’s/Men’s] Group (only if it does not fit into one of the other categories)'),
		)

		

Individual = (
			('Parents/Caregivers', 'Parents/Caregivers'),
		 	('Household Members', 'Household Members'),
			('People in Government', 'People in Government'),
			('People in USG Private Sector Assisted Firms', 'People in USG Private Sector Assisted Firms'),
			('People in Civil Society','People in Civil Society'),
			('Laborers', 'Laborers'),
			('Producers (Smallholder)', 'Producers (Smallholder)'),
			('Producer (Non-Smallholder)', 'Producer (Non-Smallholder)'),
			('Producer (Aquaculture)', 'Producer (Aquaculture)'),
			('Producer (Size Disaggregate Not Available)', 'Producer (Size Sisaggregate not Available)'),
			('Individual Type (Not Applicable)', 'Individual Type Not Applicable'),
			('Disaggregate Not Available', 'Disaggregate Not Available'),
		  )

Status =( ('Husband','Husband'),
		  ('Wife','Wife'),
		  ('Mother','Mother'),
		  ('Son','Son'),
		  ('Daughter','Daughter'),
		  ('Son/Daughter-in-Law','Son/Daughter-in-Law'),
		  ('Grandchild','Grandchild'),
		  ('Other Relative','Other Relative'),
		 )

Livelihood = (
			  ('Pastoralist', 'Pastoralist'),
			  ('Agro-Pastoralist','Agro-Pastoralist'),
			  ('Fishermen','Fishermen'),
			  ('Trader','Trader'),
			  ('Others','Others (Specify)'), 
			 )

Gender = (
		  ('Male','Male'),
		  ('Female','Female'),
)



# Overriding the Default Django Auth
# User and adding One More Field (user_type)
class CustomUser(AbstractUser):
	HOD = '1'
	STAFF = '2'
	
	EMAIL_TO_USER_TYPE_MAP = {
		'hod': HOD,
		'staff': STAFF,
	}

	user_type_data = ((HOD, "HOD"), (STAFF, "Staff"),)
	user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class AdminHOD(models.Model):
	id = models.AutoField(primary_key=True)
	admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()


class Staffs(models.Model):
	id = models.AutoField(primary_key=True)
	admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
	address = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()



class County(models.Model):
	county_id = models.IntegerField(primary_key=True)
	county_name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()

class Sub_County(models.Model):
	county = models.ForeignKey(County, on_delete=models.CASCADE)
	sub_county_id = models.IntegerField(primary_key=True)
	sub_county_name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()

class Ward(models.Model):
	county = models.ForeignKey(County, on_delete=models.CASCADE)
	sub_county = models.ForeignKey(Sub_County, on_delete=models.CASCADE)
	ward_id = models.IntegerField(primary_key=True)
	ward_name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()

class Village(models.Model):
	county = models.ForeignKey(County, on_delete=models.CASCADE)
	sub_county = models.ForeignKey(Sub_County, on_delete=models.CASCADE)
	ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
	village_id = models.IntegerField(primary_key=True)
	vllage_name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()




class HouseHold(models.Model):
	county = models.ForeignKey(County, on_delete=models.CASCADE)
	sub_county = models.ForeignKey(Sub_County, on_delete=models.CASCADE)
	ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
	village = models.ForeignKey(Village, on_delete=models.CASCADE)
	#household_id = models.IntegerField(primary_key=True)
	household_name = models.CharField(max_length=255)
	household_size = models.IntegerField()
	gps_coordinates = models.DecimalField(max_digits=22,decimal_places=16)
	# House Head Details
	participant_id = models.IntegerField(primary_key=True)        
	first_name = models.CharField(max_length=255)
	middle_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	dob = models.DateTimeField()
	age = models.IntegerField()
	sex = models.CharField(max_length=20,choices=Gender, default = 'Male')
	group_membership = models.CharField(max_length=255,choices=Group,default = None, blank=True)
	id_number = models.CharField(max_length=255)
	phone_number = models.CharField(max_length=255)
	individual_type = models.CharField(max_length=255,choices=Individual,default = None)
	registration_date = models.DateTimeField(auto_now_add=True)
	livelihood_status = models.CharField(max_length=255,choices=Livelihood,default = None)
	objects = models.Manager()



class Participant(models.Model):
	participant_id = models.IntegerField(primary_key=True)
	first_name = models.CharField(max_length=255)
	middle_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255, blank=True)
	relationship_HH = models.CharField(max_length = 30,choices=Status, default = None, null=False)
	dob = models.DateTimeField()
	age = models.IntegerField()
	sex = models.CharField(max_length = 30,choices=Gender, default = 'Male')
	group_membership = models.CharField(max_length=255,choices=Group,default = None, blank=True)
	id_number = models.CharField(max_length=255)
	phone_number = models.CharField(max_length=255)
	individual_type = models.CharField(max_length=255,choices=Individual,default = None, null=False)
	registration_date = models.DateTimeField(auto_now_add=True)
	livelihood_status = models.CharField(max_length=255,choices=Livelihood,default = None, null=False)
	objects = models.Manager()


class Groups(models.Model):
	county = models.ForeignKey(County, on_delete=models.CASCADE)
	sub_county = models.ForeignKey(Sub_County, on_delete=models.CASCADE)
	ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
	vllage = models.ForeignKey(Village, on_delete=models.CASCADE)
	group_id = models.AutoField(primary_key=True)
	group_name = models.CharField(max_length=255,default = None, null=False)
	group_leader_name = models.CharField(max_length=255,default = None, null=False)
	group_leader_phone = models.CharField(max_length=255,default = None, null=False)
	partner_name = models.CharField(max_length=255,default = None, null=False)
	registration_date = models.DateTimeField(auto_now_add=True)
	objects = models.Manager()


#Creating Django Signals
@receiver(post_save, sender=CustomUser)

# Now Creating a Function which will
# automatically insert data in HOD, Staff
def create_user_profile(sender, instance, created, **kwargs):
	# if Created is true (Means Data Inserted)
	if created:
	
		# Check the user_type and insert the data in respective tables
		if instance.user_type == 1:
			AdminHOD.objects.create(admin=instance)
		if instance.user_type == 2:
			Staffs.objects.create(admin=instance)

	

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
	if instance.user_type == 1:
		instance.adminhod.save()
	if instance.user_type == 2:
		instance.staffs.save()
